from django.utils import timezone
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


# @receiver(user_logged_in)
def update_last_login(sender, auth_user, **kwargs):
    auth_user.last_login = timezone.now()
    auth_user.save(update_fields=['last_login'])
