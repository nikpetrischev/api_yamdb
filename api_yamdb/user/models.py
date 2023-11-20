from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

CHOICES = (("user", "user"), ("moderator", "moder"), ("admin", "admin"))


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=16, choices=CHOICES, default="user")
    confirmation_code = models.CharField(null=True, max_length=40, blank=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
