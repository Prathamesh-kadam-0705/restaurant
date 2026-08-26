from django.urls import path

from .views import (
    ChangePasswordView,
    ForgotPasswordView,
    GoogleCallbackView,
    GoogleLoginView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
    UserListView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("logout/", LogoutView.as_view()),

    path("google/", GoogleLoginView.as_view(), name="google-login"),
    path(
        "google/callback/",
        GoogleCallbackView.as_view(),
        name="google-callback",
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
    ),
    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
    ),

    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]