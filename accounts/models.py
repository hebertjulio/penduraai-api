from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from model_utils.models import TimeStampedModel
from model_utils import Choices

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

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

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

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

    ROLE = Choices(
        ('owner', _('owner')),
        ('guest', _('guest')),
    )

    pin_validator = RegexValidator(r'\d{4}')

    name = models.CharField(_('name'), max_length=30)
    pin = models.CharField(_('pin'), max_length=4, validators=[pin_validator])

    accountable = models.ForeignKey(
        'User', on_delete=models.CASCADE,
        related_name='profiles_accountable',
    )

    role = models.CharField(
        _('role'), max_length=30, db_index=True,
        choices=ROLE
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        unique_together = [
            ['accountable', 'pin']
        ]
