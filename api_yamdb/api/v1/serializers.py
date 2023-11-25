import re
from datetime import datetime as dt
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.db.models import Avg

from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title
from .utils import MAX_SCORE_VALUE, MIN_SCORE_VALUE


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Поле slug должно быть уникальным',
            )
        if not re.match('^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Поле slug должно соответствовать патерну ^[-a-zA-Z0-9_]+$',
            )
        if len(value) > 50:
            raise serializers.ValidationError(
                'Длина слага не может превышать 50 символов'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'

    def validate_slug(self, value):
        if Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Поле slug должно быть уникальным',
            )
        if not re.match('^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Поле slug должно соответствовать патерну ^[-a-zA-Z0-9_]+$',
            )
        if len(value) > 50:
            raise serializers.ValidationError(
                'Длина слага не может превышать 50 символов'
            )
        return value


class BaseTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(Avg('score')).get('score__avg'))
        return None


class TitleReadSerializer(BaseTitleSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()


class TitleWriteSerializer(BaseTitleSerializer):
    description = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    def validate_genre(self, value):
        if not value:
            return value
        genres = Genre.objects.all()
        for genre in value:
            if genre not in genres:
                raise serializers.ValidationError(
                    f'Жанр {genre} не найден в базе',
                )
        return value

    def validate_category(self, value):
        if value and value not in Category.objects.all():
            raise serializers.ValidationError(
                f'Категория {value} не найдена в базе',
            )
        return value

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять ещё невышедшее произведение',
            )
        return value

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.HiddenField(default=0)

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'Вы уже создали отзыв на это произведение'
            )

    def validate_score(self, value):
        if value < MIN_SCORE_VALUE or value > MAX_SCORE_VALUE:
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_SCORE_VALUE} до {MAX_SCORE_VALUE}'
            )
        return value

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Вы уже создали отзыв на это произведение',
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
