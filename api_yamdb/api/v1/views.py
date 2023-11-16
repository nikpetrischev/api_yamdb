from rest_framework import filters, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
)

# Костыль для тестирования
from rest_framework.permissions import AllowAny

from reviews.models import (
    Title,
    Category,
    Genre,
)
from .serializers import (
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
