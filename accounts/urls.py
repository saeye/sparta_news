from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListView.as_view()),
    path("<int:user_id>/", views.UserDetailView.as_view()),
    path("signup/", views.UserCreateView.as_view()),
    path("follow/<int:user_id>/", views.FollowView.as_view()),
    path("update/<int:user_id>/", views.UserUpdateView.as_view()),
    path("changepassword/", views.ChangePasswordView.as_view()),
]
