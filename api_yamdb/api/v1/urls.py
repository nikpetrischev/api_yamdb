from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.v1.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
)


v1_router = DefaultRouter()
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]
