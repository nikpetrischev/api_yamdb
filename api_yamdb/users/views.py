from random import randint
import http

from rest_framework import filters, permissions
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework.decorators import action
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
# from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SignUpSerializer, TokenSerializer, UserSerializer
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
        send_mail(subject='Токен',
                  message=f'Код: {confirmation_code}',
                  from_email='cabugold288@yandex.ru',
                  recipient_list=[user.email])
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
    permission_classes = [IsAdmin, permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_field = ('username', )
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username:
            return User.objects.filter(username=username)
        return User.objects.all()
    
    # @action(methods=['GET', 'PATCH'],
    #         detail=False,
    #         permission_classes=[permissions.IsAuthenticated])
    # def me(self, request):
    #     serializer = UserSerializer(request.user)
    #     if request.method == 'PATCH':
    #         serializer = UserSerializer(
    #             request.user,
    #             data=request.data,
    #             partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(role=request.user.role)
    #     return Response(serializer.data)


class QurentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        # Хотя если используем partial=True - надо ли сохранять роль?
        return Response(serializer.data)
    
