import random
from django.core.mail import send_mail


def generate_verification_code():
    return ''.join(random.choices('0123456789', k=6))


def send_verification_email(email, code):
    subject = '회원가입 인증 코드'
    message = f'회원가입 인증 코드: {code}'
    from_email = 'gpting123@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
