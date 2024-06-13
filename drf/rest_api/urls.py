from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    # path('posts/', views.PostsView),
    # path('detail/<int:pk>/',views.posts_detail),
    # path('posts/', views.PostAPIView.as_view(), name='postsApiView'),
    # path('detail/<int:pk>/', views.PostDetailAPIView.as_view(), name='detailApiView'),
    path('genericApiView/<int:id>/', views.genericApiView.as_view(), name='genericApiView'),
    path('', include(router.urls))
]
