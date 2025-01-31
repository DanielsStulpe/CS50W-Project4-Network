
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path('user/<str:user>/', views.user_page, name='user_page'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>/", views.edit, name="edit"),
    path("like/<int:post_id>/", views.like, name="like"),
]
