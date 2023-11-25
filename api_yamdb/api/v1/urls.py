from django.urls import path, include

from rest_framework import routers

from .views import (
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    UserModelViewSet,
    SignUpAPIView,
    TokenAPIView,
)


router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    'Review',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    'Comment',
)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(
    r'users',
    UserModelViewSet,
    basename='users'
)

urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view()),
    path('auth/token/', TokenAPIView.as_view()),
    path('', include(router_v1.urls)),
]
