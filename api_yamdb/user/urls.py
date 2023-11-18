from django.urls import path

from .views import SignUpAPIView, TokenAPIView

urlpatterns = [
    path('v1/auth/signup/', SignUpAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),
]
