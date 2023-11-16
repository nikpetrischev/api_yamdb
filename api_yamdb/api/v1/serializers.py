from datetime import datetime as dt

from rest_framework import serializers

from reviews.models import (
    Title,
    Category,
    Genre,
    TitleGenre,
)


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
    genre = GenreSerializer(
        many=True,
        read_only=False,
        allow_null=True,
    )
    category = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        read_only=False,
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'

    def create(self, validated_data):
        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data)

        for genre in genres:
            # ToDo: Пока сомневаюсь, так или через exists с возможной ошибкой
            current_genre, status = Genre.objects.get_or_create(**genre)
            TitleGenre.objects.create(title=title, genre=current_genre)

        return title

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять ещё невышедшее произведение',
            )
        return value
