from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    #path("api/",  UsersView.as_view(), name="users-api"),
    path("api/user-login/<str:last_name>/<str:department>/<str:password>/", UserLogin.as_view(), name="user-login"),
    path("api/user-update-active/<str:last_name>/<int:active>", UserUpdateActive.as_view(), name="user-update-active"),
    path("api/user-register/<str:last_name>/<str:first_name>/<str:middle_name>/<str:position>/<str:department>/<str:password>/",
        UserRegistration.as_view(), name="user-registration"),
    path("download_file/", download_file, name="download_file")
]