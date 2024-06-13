from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

router = routers.DefaultRouter()
router.register('application', views.JobApplicationView, basename='application')

urlpatterns = [
    # url for myapp
    path('', views.Joblist.as_view(),name='index'),
    path('index', views.Joblist.as_view(),name='index'),
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(),name='logout'),
    path('signup/', views.RegisterView.as_view(),name='signup'),
    path('jobslist/', views.Jobslist.as_view(),name='jobslist'),
    path('publish/', views.PublishOfferView.as_view(),name='publish'),
    path('apply/<int:id>/', views.ApplyToOffer.as_view(),name='apply'),
    path('myapplication/', views.CurrentApplication.as_view(),name='myapplication'),
    path('myapplication/delete/<int:id>', views.CurrentApplicationDelete.as_view(),name='delapplication'),



    
    # urls for api
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('signin/', views.SigninUserView.as_view(),name="signin"),
    path('signup/', views.SignupUserView.as_view(), name="signup"),
    path('jobs/', views.JobListCreateUpdateView.as_view(), name='jobs'),
    # path('jobslist/', views.JobListView.as_view(), name='jobslist'),
    path('jobs/<int:id>/', views.JobListCreateUpdateView.as_view(), name='jobs'),
    path('del_app/<int:id>/', views.CurrentUserPostsAPIView.as_view(), name="del_app"),
    path('get_app/', views.CurrentUserPostsAPIView.as_view(), name="get_application"),
    path('',include(router.urls))
]
