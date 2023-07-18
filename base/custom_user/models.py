from django.contrib.auth.models import AbstractUser
from django.db import models

from base.custom_user.managers import UserManager


class User(AbstractUser):
    """
    Base User model which only contains an overwritten email
    field to set it as unique, since we want users to login
    using their email instead of their username.
    """

    email = models.EmailField("email address", blank=True, unique=True)
    # Set username as NOT unique so it can be left empty.
    username = models.CharField(
        "username",
        max_length=150,
        unique=False,
        null=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "auth_user"
