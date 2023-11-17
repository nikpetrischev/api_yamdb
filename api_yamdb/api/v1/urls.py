from django.urls import path, include

from rest_framework import routers

from .views import (
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
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

urlpatterns = [
    path('', include(router_v1.urls)),
]
