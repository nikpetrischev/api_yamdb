from .serializers import SignUpSerializer, TokenSerializer
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.response import Response
from random import randint
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
import http
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
import uuid







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
            user, _ = User.objects.get_or_create(email=email, username=username)
        except IntegrityError:
            raise ValidationError(detail='Invalid request data!')

        # confirmation_code = self.make_token(user)
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
    
    # @staticmethod
    # def make_token(user: User) -> uuid.UUID:
    #     confirmation_code: uuid.UUID = uuid.uuid4()
    #     user.confirmation_code = confirmation_code
    #     user.save()
    #     return confirmation_code


class TokenAPIView(APIView):
    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid()
        # raise_exception=True


        username = serializer.validated_data.get('username')
        print(username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        print('AAAAAAAAAAA')
        user = User.objects.get(username=username)
        print(user)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь не существует.'}, status=http.HTTPStatus.NOT_FOUND)
        
        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=http.HTTPStatus.CREATED)
        return Response({'confirmation_code': ['Неверный токен!']}, status=http.HTTPStatus.BAD_REQUEST)





def Send_mail(request):
    rand_int = randint(1000, 9999)
    send_mail(
        'проверка',
        f'код: {rand_int}',
        'cabugold288@yandex.ru',
        ['cabugold@mail.ru'],
        fail_silently=False,
        )
    return render('defccasd')

# @api_view(['POST'])
# def hello(request):
#     if request.method == 'POST':
#         return Response({'message': 'Получены данные', 'data': request.data})

#     return Response({'message': 'Это был GET-запрос!'}) 

# class hello(api_view)

class Auth(CreateAPIView):
    permission_classes=()
    def post(self, request, *args, **kwargs):

        rand_int = randint(1000, 9999)
        send_mail(
        'проверка',
        f'код: {rand_int}',
        'cabugold288@yandex.ru',
        ['cabugold@mail.ru'],
        )
        print(request)
        print("AAAAAAA")
        print(kwargs)
        return True
    
# from rest_framework import permissions
# from rest_framework.generics import CreateAPIView
# from django.contrib.auth import get_user_model # If used custom user model

# from .serializers import UserSerializer


# class CreateUserView(CreateAPIView):

#     model = CustomUser
#     permission_classes = [
#         permissions.AllowAny # Or anon users can't register
#     ]
#     serializer_class = UserSerializer