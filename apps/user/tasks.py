from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from apps.user.utils import generate_random_verification_code
from config.settings import base

USER_MODEL=get_user_model()
@shared_task(bind=True)
def send_verification_message(self,user_id):
    try:
        user=USER_MODEL.objects.get(id=user_id)
        code=generate_random_verification_code(6)
        subject="Account Verification"
        to=[user.email]
        from_email=settings.EMAIL_BACKEND
        message=f"Your verification code is {code}.Please verify your account.Thankyou"
        html_string=render_to_string("email/email_verification.html",{"user":user,"code":code})
        msg=EmailMultiAlternatives(subject,message,from_email=from_email,to=to)
        msg.attach_alternative(html_string,"text/html")
        msg.send()
    except USER_MODEL.DoesNotExist:
        raise ValueError("User doesn't exist")

    except Exception as e:
        self.retry(
            exc=e,
            countdown=10,
            max_retries=3
        )