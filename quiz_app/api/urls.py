from django.urls import path

from .views import AttemptView, LoginAPIView, ProfileView, QuizListView, SignupAPIView

urlpatterns = [
    path("auth/signup/", SignupAPIView.as_view()),
    path("auth/login/", LoginAPIView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("quizzes/", QuizListView.as_view()),
    path("attempt/", AttemptView.as_view()),
]
