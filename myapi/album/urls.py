from django.urls import path, include
from .views import TrackViewsets, AlbumViewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('album', AlbumViewsets, basename='album')
router.register('track', TrackViewsets, basename='track')

urlpatterns = [
    path('', include(router.urls))
]
