from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from utils.models.validators import BlackListValidator

from .managers import UserManager


class User(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    email = models.EmailField(
        blank=False,
        null=False,
        unique=True
    )

    username_validator = UnicodeUsernameValidator()
    blacklist_validator = BlackListValidator(['me'], 'Username not allowed.')
    username = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        unique=True,
        validators=[username_validator, blacklist_validator]
    )

    created_at = models.DateTimeField(default=timezone.now)

    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

