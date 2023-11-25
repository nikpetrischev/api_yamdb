from random import randint
import http

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.mail import send_mail

from rest_framework import filters, viewsets, status, permissions
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action

# Костыль для тестирования
from rest_framework.permissions import AllowAny
from reviews.models import Category, Genre, Review, Title

# from .permissions import (
#     IsAdminOrModeratorOrAuthorOrReadOnly,
# )
from .filters import TitleFilter
# from .permissions import IsAdmin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
)
from .permissions import IsAdmin

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
                email=email,
                username=username
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
        FROM_EMAIL = 'cabugold288@yandex.ru'
        RECIPIENT_LIST = [user.email]

        send_mail(subject=SUBJECT,
                  message=MESSAGE,
                  from_email=FROM_EMAIL,
                  recipient_list=RECIPIENT_LIST)
        return Response(
            {'email': f'{email}', 'username': f'{username}'},
            status=http.HTTPStatus.OK
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
                status=http.HTTPStatus.NOT_FOUND
            )

        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=http.HTTPStatus.CREATED
            )
        return Response(
            {'confirmation_code': ['Неверный токен!']},
            status=http.HTTPStatus.BAD_REQUEST
        )


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username:
            return User.objects.filter(username=username)
        return User.objects.all()

    @action(detail=False,
            url_path='me',
            methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save(role=request.user.role)
        return Response(serializer.data)

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
    # queryset = (Title.objects.all().order_by('id')
    #             .select_related('category').prefetch_related('genre'))
    queryset = Title.objects.all().order_by('id')
    filterset_class = TitleFilter
    permission_classes = [
        AllowAny,
    ]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TitleReadSerializer
        return TitleWriteSerializer

    # Запоминаем тайтл, чтоб каждый раз не обращаться запросом к БД
    def get_object(self):
        if not self._title:
            self._title = super().get_object()
        return self._title

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().update(request, *args, **kwargs)


class GenreViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [
        # IsAdmin,
        AllowAny,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [
        # IsAdmin,
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
