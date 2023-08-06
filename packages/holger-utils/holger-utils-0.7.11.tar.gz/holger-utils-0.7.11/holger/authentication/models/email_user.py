from .abstract_user import AbstractUser


class EmailUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        if not self.pk:
            super(EmailUser, self).save(*args, **kwargs)
            self.send_verification_code()
        else:
            super(EmailUser, self).save(*args, **kwargs)
