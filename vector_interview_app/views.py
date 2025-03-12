from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import UserSignUpSerializer
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.contrib.auth import login,authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect,render
from django.contrib import messages
from .serializers import InterviewSerializer
from .models import Interview

class UserSignUpView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "signup.html"
    def get(self,format=None):
        serializer = UserSignUpSerializer()
        return Response({"serializer": serializer})
    
    def post(self, request, format=None):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request,user)
            if request.accepted_renderer.format == 'html':
                messages.success(request,"Sign up successfully")
                return redirect('login')
            else: 
                refresh = RefreshToken.for_user(user)
                data ={
                "detail": "User created successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh)

                }
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'serializer': serializer},status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'login.html'  # Create this template in your templates folder

    def get(self, request, format=None):
        # Render an empty login form
        return Response({}, template_name=self.template_name)

    def post(self, request, format=None):
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
                messages.error(request,"Invalid credentials. please try again")
                return render(request, self.template_name)
            else:
                error_data = {"detail": "Invalid credentials"}
                return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return render(request,'home.html',{})

class InterviewCreateAPIView(generics.CreateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer