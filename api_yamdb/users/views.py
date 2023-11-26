from rest_framework import filters, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from api.v1.permissions import IsAdmin
from .serializers import UserSerializer

User = get_user_model()


class UserModelViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [
        IsAdmin,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username:
            return User.objects.filter(username=username)
        return User.objects.order_by('id')

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save(role=request.user.role)
        return Response(serializer.data)
