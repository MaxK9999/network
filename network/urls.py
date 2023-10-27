
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("create_comment/<int:post_id>", views.create_comment, name="create_comment"),
    path("load_posts", views.load_posts, name="load_posts"),
]
