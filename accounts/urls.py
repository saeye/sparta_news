from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserCreateView.as_view()),
    path("follow/<int:user_id>/", views.FollowView.as_view()),
    path("update/<int:user_id>/", views.UserUpdateView.as_view()),
]
