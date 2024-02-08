
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/create", views.create_post, name="create_post" ),
    path("posts/like", views.like_post, name="like_post"),
    path("following", views.following_view, name="following"),
    path("<str:username>", views.profile_view, name="profile"),
    path("follow/<str:user_id>", views.follow, name="follow"),
]
