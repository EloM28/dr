from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic.edit import View
from rest_framework import status
import logging
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate,login, logout
from django.middleware.csrf import get_token


class UserRegistrationView(APIView):
    permission_classes = []
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        print(f'the serializer datas are :{serializer}')
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


logger = logging.getLogger(__name__)

class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['userName']
        password = request.POST['password']
        print(f'datas are :{username} and {password}')
        user = authenticate(request, username=username, password=password)
        print(f'user found is : {user}')
        if user:
            login(request, user)
            next_url = request.GET.get("redirect_to")
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
            # return render(request, 'dashboard.html')
        return render(request, 'login.html', {'error': 'Identifiants invalides'})

class LogoutView(View):
    def get(self, request):
        logger.info(f"user {self.request.user.email} disconnected")
        logout(request)
        return redirect("/docteur/login")

class DashboardView(LoginRequiredMixin, View):
    login_url = "/docteur/login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, 'dashboard.html')


def home(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')
def dashboard(request):
    return render(request,'dashoard.html')