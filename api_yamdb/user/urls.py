from .views import SignUpAPIView, TokenAPIView

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

router_v1 = SimpleRouter

# router_v1.register('', View, basename='')

urlpatterns = [
    path('v1/auth/signup/', SignUpAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),

    path('v1/', include('djoser.urls.jwt')),
    # path('v1/', include(router_v1.urls)),
    # path('v1/auth/signup/', Auth.as_view()),
    # path('v3/', Send_mail),
]