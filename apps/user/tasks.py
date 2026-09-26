from linecache import cache


from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from apps.user.services import VerificationService
from apps.user.utils import generate_random_verification_code

USER_MODEL=get_user_model()
@shared_task(bind=True)
def send_verification_message(self,user_id):
    try:
        VerificationService().save_verification_code(user_id,code)
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
@shared_task(bind=True)
def send_reset_link_message(self,token,user_id):
    try:
        user=USER_MODEL.objects.get(id=user_id)
        link_url=f"{settings.FRONTEND_URL}/reset/{user_id}/{token}"
        VerificationService.set_reset_key(user_id,token)
        subject="Reset Password Request"
        to=[user.email]
        from_email=settings.EMAIL_BACKEND
        message=f"Your reset link is {link_url}.You can open this link to reset your password"
        html_string=render_to_string("email/reset_email.html",{"user":user,"reset_link":link_url})
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