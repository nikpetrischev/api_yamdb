# Django Library
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

CHOICES = (
    (USER, "user"),
    (MODERATOR, "moder"),
    (ADMIN, "admin")
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.CharField(max_length=254, blank=True)
    role = models.CharField(max_length=16, choices=CHOICES, default=USER)
    confirmation_code = models.CharField(null=True, max_length=40, blank=True)

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
