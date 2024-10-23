import openai
from django.conf import settings
from accounts.models import User
from django.core.management.base import BaseCommand
from matches.models import Match

class Command(BaseCommand):
    help = 'Generate matches using LLM recommendations'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            recommended_users = self.get_llm_recommendations(user)
            for recommended_user in recommended_users:
                Match.objects.get_or_create(
                    user1=user,
                    user2=recommended_user,
                    defaults={'user1_likes_user2': False, 'user2_likes_user1': False, 'is_mutual': False}
                )

    def get_llm_recommendations(self, user):
        # OpenAI API 키 설정
        openai.api_key = settings.OPENAI_API_KEY
        
        # 예시 프롬프트: 사용자 매칭을 위한 적절한 프롬프트 작성
        prompt = f"사용자 {user.username}에게 적합한 5명의 매칭 사용자 추천."

        try:
            # OpenAI API 호출
            response = openai.Completion.create(
                engine="text-davinci-003",  # 적절한 엔진 선택
                prompt=prompt,
                max_tokens=150,
                n=5,  # 추천할 사용자 수
                stop=None,
                temperature=0.7
            )

            # 응답에서 추천 사용자 추출
            recommendations = response.choices[0].text.strip().split('\n')
            
            # 추천된 사용자명을 User 객체로 변환 (사용자명이 반환된다고 가정)
            recommended_users = User.objects.filter(username__in=recommendations)

            return recommended_users

        except Exception as e:
            self.stderr.write(f"Error generating recommendations for {user.username}: {e}")
            return []
