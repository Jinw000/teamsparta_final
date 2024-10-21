"""Authentication classes for channels."""
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from jwt import decode as jwt_decode
import jwt

User = get_user_model()

class JWTAuthMiddleware:
    """Middleware to authenticate user for channels"""

    def __init__(self, app):
        """Initializing the app."""
        self.app = app

    async def __call__(self, scope, receive, send):

        """Authenticate the user based on jwt."""
        close_old_connections()
        try:
            token = parse_qs(scope["query_string"].decode(
                    "utf8")).get('token', None)[0] 

            # Decode the token to get the user id from it.
            data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user_id = data.get('user_id')  # 토큰 페이로드에서 user_id 추출

            if user_id:
                        # user_id를 통해 데이터베이스에서 사용자 정보를 가져옴
                scope['user'] = await self.get_user(user_id)

            else:
                scope['user'] = AnonymousUser() # scope['user']에 정보가 담김

        except (InvalidSignatureError, ExpiredSignatureError, DecodeError, KeyError) as e:
                # 토큰이 잘못되었거나 만료된 경우 익명 사용자로 설정
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        """데이터베이스에서 user_id에 해당하는 사용자를 가져옵니다."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    """This function wrap channels authentication stack with JWTAuthMiddleware."""
    return JWTAuthMiddleware(AuthMiddlewareStack(app))