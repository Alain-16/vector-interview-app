"""
User Authentication and Interview API Views

This module provides API endpoints for user signup, login, and interview creation.
It supports both HTML and JSON responses and integrates JWT authentication.

Features:
- User signup with password validation
- User login with JWT authentication
- Render HTML templates for web-based responses
- Secure interview creation using Django REST Framework (DRF)
"""

from rest_framework import generics, status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect, render
from django.contrib import messages
from .serializers import UserSignUpSerializer, InterviewSerializer
from .models import Interview
from .pagination import CustomPagination

class UserSignUpView(APIView):
    """
    Handles user signup.

    - Supports both HTML and JSON responses.
    - Saves a new user if validation is successful.
    - Returns a JWT access and refresh token upon successful signup.
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "signup.html"

    def get(self, request, format=None):
        """Returns an empty serializer for HTML form rendering."""
        serializer = UserSignUpSerializer()
        return Response({"serializer": serializer})
    
    def post(self, request, format=None):
        """Processes user signup and returns authentication tokens."""
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            if request.accepted_renderer.format == 'html':
                messages.success(request, "Sign up successfully")
                return redirect('login')
            else:
                refresh = RefreshToken.for_user(user)
                data = {
                    "detail": "User created successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
                return Response(data, status=status.HTTP_201_CREATED)
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    Handles user login.

    - Supports both HTML and JSON responses.
    - Authenticates the user and returns JWT tokens.
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'login.html'

    def get(self, request, format=None):
        """Returns an empty login form for HTML rendering."""
        return Response({}, template_name=self.template_name)

    def post(self, request, format=None):
        """Processes user login and returns authentication tokens."""
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.accepted_renderer.format == 'html':
                messages.success(request, "Logged in successfully")
                return redirect('home')
            else:
                refresh = RefreshToken.for_user(user)
                data = {
                    "detail": "Logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
                return Response(data, status=status.HTTP_200_OK)
        else:
            if request.accepted_renderer.format == 'html':
                messages.error(request, "Invalid credentials. Please try again")
                return render(request, self.template_name)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    """Renders the home page template."""
    return render(request, 'home.html', {})

class InterviewController(viewsets.ModelViewSet):
    """
    Handles interview creation.

    - Requires authentication.
    - Uses DRF's CreateAPIView for simplified creation logic.
    - Only authorized users can create interviews.
    """
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    pagination_class=CustomPagination
