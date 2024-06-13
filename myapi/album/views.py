from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Track, Album
from .serializer import AlbumSerializer, TrackSerializer

# Create your views here.

class AlbumViewsets(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        albums = Album.objects.all()
        return albums

class TrackViewsets(viewsets.ModelViewSet):
    serializer_class = TrackSerializer

    def get_queryset(self):
        tracks = Track.objects.all()
        return tracks