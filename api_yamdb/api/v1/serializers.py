from datetime import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Поле slug должно быть уникальным',
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()

    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'

    def validate_slug(self, value):
        if Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Поле slug должно быть уникальным',
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    decription = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    genre = SlugRelatedField(
        allow_null=True,
        many=True,
        queryset=Genre.objects.all(),
        read_only=False,
        slug_field='slug',
    )
    category = serializers.SlugRelatedField(
        allow_null=True,
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def create(self, validated_data):
        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data)

        for genre in genres:
            TitleGenre.objects.create(title=title, genre=genre)

        return title

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

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(Avg('score')).get('score__avg'))
        return None


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
