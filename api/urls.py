from django.urls import path

from api.views import ListTaskApi, RegisterUserApi, LoginUserApi

urlpatterns = [
    path("list-task/", ListTaskApi.as_view()),
    path("register-user/", RegisterUserApi.as_view()),
    path("login-user/", LoginUserApi.as_view()),
]
