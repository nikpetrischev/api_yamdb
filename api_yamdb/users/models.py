# Django Library
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.CharField(max_length=254, blank=True)
    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.USER
    )
    confirmation_code = models.CharField(null=True, max_length=40, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR
