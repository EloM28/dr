from .import views
from django.urls import path
from .views import UserRegistrationView, LoginView, DashboardView, LogoutView, PredictView, PredictAPIView, LoginAPIView




urlpatterns = [
    # path("",DashboardView.as_view(), name="home"),
    
    path("register/", UserRegistrationView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("dashboard/",DashboardView.as_view(), name="dashboard"),
    path("api/predict/",PredictAPIView.as_view(),name='api_predict'),
    path("predict/", PredictView.as_view(), name='predict'),
    
    
    # API Routes
    
    path("api/login/", LoginAPIView.as_view(), name='api_login'),
    
]
