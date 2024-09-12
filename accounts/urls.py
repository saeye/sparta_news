from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [   
    path("", views.UserListView.as_view()()),
    path("<int:user_id>/", views.UserDetailView.as_view()),
    path("signup/", views.UserCreateView.as_view()),
    path("signin/", views.SigninView.as_view()),
    path("signout/", views.SignoutView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),   
    path("follow/<int:user_id>/", views.FollowView.as_view()),
    path("update/<int:user_id>/", views.UserUpdateView.as_view()),
    path("changepassword/", views.ChangePasswordView.as_view()),
    path("deleteuser/", views.DeleteUserView.as_view()),
]
