import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User
from .serializers import ChangePasswordSerializer, ForgotPasswordSerializer, LoginSerializer, RegisterSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.http import JsonResponse
from urllib.parse import urlencode

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import secrets


class UserListView(APIView):

    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data,
                },
                status=201,
            )

        return Response(serializer.errors, status=400)


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login successful",

                "access": str(refresh.access_token),

                "refresh": str(refresh),

                "user": UserSerializer(user).data,
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "message": "You are authenticated",
            "user": UserSerializer(request.user).data,
        })

class LogoutView(APIView):

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )



class GoogleLoginView(APIView):

    def get(self, request):
        google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"

        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account",
        }

        url = f"{google_auth_url}?{urlencode(params)}"

        return JsonResponse({
            "url": url
        })

class GoogleCallbackView(APIView):

    def get(self, request):

        code = request.GET.get("code")

        if not code:
            return Response(
                {"error": "Authorization code is missing"},
                status=400,
            )

        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )

        token_data = token_response.json()

        if "id_token" not in token_data:
            return Response(
                {
                    "error": "Could not get Google ID token",
                    "details": token_data,
                },
                status=400,
            )

        google_id_token = token_data["id_token"]

        try:
            google_user = id_token.verify_oauth2_token(
                google_id_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )

        except ValueError:
            return Response(
                {"error": "Invalid Google ID token"},
                status=400,
            )

        email = google_user.get("email")

        if not email:
            return Response(
                {"error": "Google account email not available"},
                status=400,
            )

        user, created = User.objects.get_or_create(
            email=email
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Google login successful",
            "created": created,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        })

class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():

            user = request.user

            user.set_password(
                serializer.validated_data["new_password"]
            )

            user.save()

            return Response({
                "message": "Password changed successfully"
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class ForgotPasswordView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["email"]

            try:
                user = User.objects.get(email=email)

                token = secrets.token_urlsafe(32)

                # For now, just return the token.
                # Later we will email this token.
                return Response({
                    "message": "Password reset token generated",
                    "token": token,
                })

            except User.DoesNotExist:
                return Response({
                    "message": "If this email exists, a reset link will be sent."
                })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )