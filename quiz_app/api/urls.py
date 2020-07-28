from django.urls import path

from .views import LoginAPIView, SignupAPIView

urlpatterns = [
    path('auth/signup/', SignupAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
]
