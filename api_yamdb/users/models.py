# Django Library
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

CHOICES = (("user", "user"), ("moderator", "moder"), ("admin", "admin"))
'''
REVIEW
Лучше будет сделать поле выбора следующим образом:
https://stackoverflow.com/a/59199143/15843456
Так у вас появится возможность сравнивать не строки (как, например у вас
сделано в permissions, а какие-то константы. Это обычный принцип DRY - вы
реализуете логику 1 раз (в данном случае имена ролей) и потом используете её
везде. Это сильно уменьшает возможность возникновения ошибки.
'''


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
    '''
    REVIEW
    Нужно использовать строковую константу из будущего варианта CHOICES
    '''

    @property
    def is_moderator(self):
        return self.role == 'moderator'
    '''
    REVIEW
    См выше
    '''
