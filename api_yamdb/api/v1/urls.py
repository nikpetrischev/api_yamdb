from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

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

urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
]
