from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from model_utils.models import TimeStampedModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=50)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    @staticmethod
    def get_fields():
        return User._meta.get_fields()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Profile(TimeStampedModel):

    PIN_REGEX = r'\d{4}'

    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(_('name'), max_length=30)

    pin = models.CharField(_('pin'), max_length=4, validators=[
        RegexValidator(PIN_REGEX)
    ], db_index=True)

    accountable = models.ForeignKey(
        'User', on_delete=models.CASCADE,
        related_name='profiles',
    )

    is_owner = models.BooleanField(
        _('owner status'),
        default=False,
        help_text=_(
            'Designates whether the profile is from account owner.'),
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this profile should be treated as active. '
            'Unselect this instead of deleting profile.'
        ),
    )

    can_manage = models.BooleanField(_('can manage'))
    can_attend = models.BooleanField(_('can attend'))
    can_buy = models.BooleanField(_('can buy'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
