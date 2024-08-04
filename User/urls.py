from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),

    path('login/', login, name="login"),
    path('register/', register_attempt, name="register_attempt"),
    path('token/', token_send, name="token_send"),
    path('verify/<auth_token>', verify, name="verify"),
    path('logout/', logout_private_admin, name="logout"),

    path('password-reset/', reset_password, name="password-reset"),
    path('change-password/', change_password, name='change_password')
]
