from .import views
from django.urls import path
from .views import UserRegistrationView, LoginView, DashboardView, LogoutView




urlpatterns = [
    path("home/",views.home,name="home"),
    
    path("register/", UserRegistrationView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("dashboard/",DashboardView.as_view(), name="dashboard"),
    path("home/",views.register,name="home"),
    path("dash/",views.dashboard,name="dash")
]
