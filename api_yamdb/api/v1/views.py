from rest_framework import filters, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
)

# Костыль для тестирования
from rest_framework.permissions import AllowAny

from reviews.models import (
    Review,
    Title,
    Category,
    Genre,
)
from permissions import CommentPermission, ReviewPermission
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
)


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        queryset = Review.objects.filter(post=self.kwargs['review_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission,)

    # def get_queryset(self):
    #     queryset = Comment.objects.filter(post=self.kwargs['post_id'])
    #     return queryset

    def perform_create(self, serializer):
        # title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        # review = get_object_or_404(Review, pk=self.kwargs['title_id'])
        # serializer.save(author=self.request.user, title=title, review=review)
