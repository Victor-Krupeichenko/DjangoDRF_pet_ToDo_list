from django.urls import path

from api.views import ListTaskApi, RegisterUserApi, LoginUserApi, TaskCreate

urlpatterns = [
    path("list-task/", ListTaskApi.as_view()),
    path("execute-status/<int:task_id>/", ListTaskApi.as_view()),
    path("register-user/", RegisterUserApi.as_view()),
    path("login-user/", LoginUserApi.as_view()),
    path("create-task/", TaskCreate.as_view()),
]
