from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from api_yamdb.settings import EMAIL_HOST_USER


def send_confirmation_code(user):
    user.confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения YaMDB'
    message = f'Ваш код для авторизации на YaMDB - {user.confirmation_code}'
    from_email = EMAIL_HOST_USER
    to_email = [user.email]
    return send_mail(subject, message, from_email, to_email)
