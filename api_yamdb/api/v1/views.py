from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response

# Костыль для тестирования
from rest_framework.permissions import AllowAny
from reviews.models import Category, Genre, Review, Title

from .permissions import (
    IsAdminOrModeratorOrAuthorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)


class CommentReviewBase(viewsets.ModelViewSet):
    def get_review(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return review

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().update(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    _title = None

    # Кверисет сортируем, чтобы пагинация давала стабильный результат
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'category__slug',
        'genre__slug',
        'name',
        'year',
    ]
    permission_classes = [
        AllowAny,
    ]

    # Запоминаем тайтл, чтоб каждый раз не обращаться запросом к БД
    def get_object(self):
        if not self._title:
            self._title = super().get_object()
        return self._title


class GenreViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ReviewViewSet(CommentReviewBase):
    serializer_class = ReviewSerializer
    permission_classes = [
        AllowAny,
    ]
    # permission_classes = (IsAdminOrModeratorOrAuthorOrReadOnly,)

    def get_queryset(self):
        queryset = Review.objects.filter(title=self.kwargs['title_id'])
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(CommentReviewBase):
    serializer_class = CommentSerializer
    permission_classes = [
        AllowAny,
    ]
    # permission_classes = (IsAdminOrModeratorOrAuthorOrReadOnly,)

    def get_queryset(self):
        review = self.get_review()
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = self.get_review()
        serializer.save(author=self.request.user, title=title, review=review)
