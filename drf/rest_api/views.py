from django.shortcuts import render 
from .models import Post
from .serializers import PostSerializer
# from django.http import JsonResponse,HttpResponse
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
# Create your views here.
# @csrf_exempt
# def PostsView(request):
#     if request.method == 'GET':
#         posts = Post.objects.all() 
#         serializer = PostSerializer(posts,many=True)
#         return JsonResponse(serializer.data , safe=False)
    
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201)
#         return JsonResponse(serializer.errors, status = 400)
    
# @csrf_exempt

# def posts_detail(request, pk):
#     try:
#         post = Post.objects.get(pk=pk) 
#     except post.DoesNotExist:
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serialize = PostSerializer(post)
#         return JsonResponse(serialize.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serialize = PostSerializer(post,data=data)

#         if serialize.is_valid():
#             serialize.save()
#             return JsonResponse(serialize.data)
#         return JsonResponse(serialize.errors, status=400)
#     elif request.method == "DELETE":
#         post.delete()
#         return HttpResponse(status=204)

# @api_view(['GET','POST'])
# def PostsView(request):
#     if request.method == 'GET':
#         posts = Post.objects.all() 
#         serializer = PostSerializer(posts,many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET','PUT','POST'])
# def posts_detail(request, pk):
#     try:
#         post = Post.objects.get(pk=pk) 
#     except post.DoesNotExist:
#         return Response(status=404)
#     if request.method == 'GET':
#         serialize = PostSerializer(post)
#         return Response(serialize.data)
#     elif request.method == 'PUT':
#         serialize = PostSerializer(post,data=request.data)

#         if serialize.is_valid():
#             serialize.save()
#             return Response(serialize.data)
#         return Response(serialize.errors, status=400)
#     elif request.method == "DELETE":
#         post.delete()
#         return Response(status=204)


# Classe_based views


class PostAPIView(APIView):
    def get(self,request ):
        posts = Post.objects.all() 
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
               raise Http404
    def get(self, request, pk):
        post = self.get_object(pk)
        serialize = PostSerializer(post)
        return Response(serialize.data)
    def put(self, request, pk):
        post = self.get_object(pk)
        serialize = PostSerializer(post,data=request.data)

        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class genericApiView(generics.GenericAPIView, 
                     mixins.ListModelMixin, 
                     mixins.CreateModelMixin, 
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # used in authentication for the browser side
    authentication_classes = [TokenAuthentication]  # used in authentication for application(mobile or desktops)
    permission_classes = [IsAuthenticated]
    def get(self, request,id):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    
    def post(self, request):
        return self.create(request)
    def put(self, request, id=None):
        return self.update(request, id)
    def delete(self, request, id=None):
        return self.destroy(request, id)
    

# class PostViewSet(viewsets.ViewSet):
#     def list(self,request):
#         posts = Post.objects.all() 
#         serializer = PostSerializer(posts,many=True)
#         return Response(serializer.data)
#     def create(self, request):
#         serializer = PostSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
     

class PostViewSet(viewsets.GenericViewSet, 
        mixins.ListModelMixin, mixins.UpdateModelMixin,
          mixins.CreateModelMixin, mixins.DestroyModelMixin,
            mixins.RetrieveModelMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self,request):
        posts = Post.objects.all() 
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    def create(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
     
