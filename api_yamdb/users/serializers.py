from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CHOICES

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name",
            "last_name", "bio", "role"
        )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length=150, regex=r'^[\w.@+-]+\Z')
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Недопустимое имя пользователя!')
        return value


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
