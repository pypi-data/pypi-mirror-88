from ..managers import PhoneStaffManager, PhoneUserManager, PhoneSuperuserManager
from django.contrib.sites.shortcuts import get_current_site
from .abstract_user import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from kavenegar import *
from django.core.exceptions import ImproperlyConfigured


class PhoneNumberUser(AbstractUser):
    sms_api = KavenegarAPI(getattr(settings, 'KAVENEGAR_API', ''))  # FIXME not supported

    cellphone = PhoneNumberField(
        verbose_name='تلفن همراه',
        region='IR',
        unique=True
    )

    first_name = models.CharField(
        _('نام'),
        max_length=100,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        _('نام خانوادگی'),
        max_length=200,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        _('ایمیل'),
        max_length=250,
        unique=True,
        blank=True,
        null=True,
        help_text=_('250 characters or fewer.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'cellphone'
    REQUIRED_FIELDS = []

    objects = PhoneUserManager()
    superusers = PhoneSuperuserManager()
    staff = PhoneStaffManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return "%s" % self.full_name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(PhoneNumberUser, self).save(*args, **kwargs)
            self.send_verification_code()
        else:
            super(PhoneNumberUser, self).save(*args, **kwargs)

    def send_verification_code(self):
        sender = getattr(settings, 'SMS_SENDER')
        if sender:
            receptor = self.cellphone
            link = self.get_magic_link
            message = "{} \n{}".format(
                'Please click on the link to confirm your verification,',
                link
            )
            context = {
                'sender': sender,
                'receptor': receptor,
                'message': message,
            }
            response = self.sms_api.sms_send(context)
        else:
            raise ImproperlyConfigured('The SMS_SENDER setting must not be empty.')
