from django.urls import path, include
from .views import StudentViewSet, ModulesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('student', StudentViewSet, basename='student')
router.register('module', ModulesViewSet, basename='module')

urlpatterns = [
    path('', include(router.urls))
]
