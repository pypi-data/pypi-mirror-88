from django.contrib import admin
from django.contrib.auth.models import Permission
from .user_admin import UserAdmin
from .phone_user_admin import PhoneUserAdmin
from ..models import EmailUser, PhoneNumberUser
from django.conf import settings

admin.site.register(Permission)

if hasattr(settings, 'AUTH_USER_MODEL') and settings.AUTH_USER_MODEL == 'holger.auth.PhoneNumberUser':
    admin.site.register(PhoneNumberUser, PhoneUserAdmin)
else:
    admin.site.register(EmailUser, UserAdmin)
