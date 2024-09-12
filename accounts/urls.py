from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserCreateView.as_view()),
    path("follow/<int:user_id>/", views.FollowView.as_view()),
]
