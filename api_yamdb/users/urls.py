from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (SignUpAPIView, TokenAPIView,
                    UserModelViewSet, QurentUserAPIView)

router_v1 = SimpleRouter()
router_v1.register(
    'users',
    UserModelViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/auth/signup/', SignUpAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),
    path('v1/users/me/', QurentUserAPIView.as_view()),
    path('v1/', include(router_v1.urls))
]
