from reviews.models import Comment, Review
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = (
            'title',
            'review',
        )
