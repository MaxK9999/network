
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    path("create_comment/<int:post_id>", views.create_comment, name="create_comment"),
    path("get_posts", views.get_posts, name="get_posts"),
    path("profile_page/<str:username>", views.profile_page, name="profile_page"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("following_page", views.following_page, name="following_page"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("get_user_posts/<str:username>", views.get_user_posts, name="get_user_posts"),
]
