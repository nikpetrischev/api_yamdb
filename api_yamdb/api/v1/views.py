# Standart Library
import http
from random import randint

# Django Library
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404

# DRF Library
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import AccessToken

# Local Imports
from .filters import TitleFilter
from .mixins import PatchNotPutModelMixin
from .permissions import IsAdminModeratorAuthorReadOnly, IsAdminOrAnon
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
)
from .utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class SignUpAPIView(APIView):
    def post(self, *args, **kwargs):
        '''Валидация и получение данных'''
        serializer = SignUpSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        '''Получене или Создание пользователя'''
        try:
            user, _ = User.objects.get_or_create(
                email=email, username=username
            )
        except IntegrityError:
            raise ValidationError(detail='Invalid request data!')

        '''Создания кода и сохранение в БД'''
        confirmation_code = randint(1000, 9999)
        user.confirmation_code = confirmation_code
        user.save()

        '''Отправка письма'''
        SUBJECT = 'Токен'
        MESSAGE = f'Код: {confirmation_code}'
        RECIPIENT_LIST = [user.email]

        send_confirmation_code(
            SUBJECT, MESSAGE,
            RECIPIENT_LIST,
        )
        return Response(
            {'email': f'{email}', 'username': f'{username}'},
            status=http.HTTPStatus.OK,
        )


class TokenAPIView(APIView):
    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'message': 'Пользователь не существует.'},
                status=http.HTTPStatus.NOT_FOUND,
            )

        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'}, status=http.HTTPStatus.CREATED
            )
        return Response(
            {'confirmation_code': ['Неверный код подтверждения!']},
            status=http.HTTPStatus.BAD_REQUEST,
        )


class TitleViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    PatchNotPutModelMixin,
    RetrieveModelMixin,
):
    _title = None

    # Кверисет сортируем, чтобы пагинация давала стабильный результат
    queryset = (
        Title.objects
        .order_by('id')
        .select_related('category')
        .prefetch_related('genre')
        .annotate(
            rating=Avg('reviews__score'),
        )
    )
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrAnon]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TitleReadSerializer
        return TitleWriteSerializer

    # Запоминаем тайтл, чтоб каждый раз не обращаться запросом к БД
    def get_object(self):
        if not self._title:
            self._title = super().get_object()
        return self._title


class GenreViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    queryset = Genre.objects.order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrAnon]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrAnon]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CommentReviewBase(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    PatchNotPutModelMixin,
    RetrieveModelMixin,
):
    def get_review(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return review


class ReviewViewSet(CommentReviewBase):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorReadOnly,)

    def get_queryset(self):
        queryset = Review.objects.filter(
            title=self.kwargs['title_id']
        ).order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(CommentReviewBase):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorReadOnly,)

    def get_queryset(self):
        review = self.get_review()
        queryset = review.comments.order_by('id')
        return queryset

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
