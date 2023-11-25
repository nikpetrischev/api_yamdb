import re
from datetime import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title


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

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = (
            'title',
            'review',
        )
