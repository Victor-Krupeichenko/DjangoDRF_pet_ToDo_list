from django.urls import path
from .views import ListTaskViews, CreateTask, RegisterUser, user_logout, LoginUser, chenge_status

urlpatterns = [
    path("", ListTaskViews.as_view(), name="home"),
    path("add-task/", CreateTask.as_view(), name="create_task"),
    path("chenge-status/<int:task_id>/", chenge_status, name="chenge_status"),
    path("register-user/", RegisterUser.as_view(), name="register_user"),
    path("login-user/", LoginUser.as_view(), name="login_user"),
    path("logout-user/", user_logout, name="logout_user"),
]
