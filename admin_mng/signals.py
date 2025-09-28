from django.contrib.auth.models import User,Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User=get_user_model()


@receiver(post_save, sender=User)  
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        print("=====signal triged=====")
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/admin_mng/activate/{instance.id}/{token}"
        print("Activation URL:",activation_url)
        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER,recipient_list)
            print("===Mail sent successfully ===")
        except Exception as er:
            print(f"Failed to send mail to {instance.email}: {str(er)}")



@receiver(post_save,sender=User)
def assign_group(sender,instance,created,**kwargs):
    if created:
        user_group,created=Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()