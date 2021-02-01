
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_post", views.new_post, name="new_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_view, name="following"),
    path("followship/<str:profile_user>", views.followship, name="followship"),
    path("<str:user>", views.profile, name="profile"),

    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("like/<int:post_id>", views.like_handler, name="like_handler"),
    
]
