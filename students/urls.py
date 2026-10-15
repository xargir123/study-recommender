
from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("quiz/", views.quiz, name="quiz"),
    path("study-plan/", views.study_plan, name="study_plan"),
    path("progress/", views.progress, name="progress"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
]