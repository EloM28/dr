from .import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, LoginView, ChangePasswordAPIViewset, DashboardView, LogoutView, PredictView, PredictAPIView, LoginAPIView

router = DefaultRouter()

router.register(r'user', ChangePasswordAPIViewset, basename='change_pass')



urlpatterns = router.urls + [
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
