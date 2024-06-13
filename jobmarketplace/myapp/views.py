from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .tokens import create_jwt_pair_for_user
from django.views.generic.edit import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth import login


from .forms import SignupForm
from .forms import SigninForm
from .models import User, JobPosting, JobApplication
from .serializers import UserSerializer
from .serializers import JobPostingSerializer
from .serializers import JobApplicationSerializer
from .serializers import UserSignupSerializer

# Create your views here.

# class JobListCreateView(viewsets.ModelViewSet):
#      serializer_class = JobPostingSerializer
#      permission_classes = [IsAuthenticated]
     
#      def get_queryset(self):
#         joblists = JobPosting.objects.all()
#         return joblists
    
#         # self.serializer_class(jobs, many=True)
#         # return Response(data=serializer.data, status=status.HTTP_200_OK)
     
#      def create(self,request):
#         data = request.data
#         user = self.request.user
#         new_job = JobPosting.objects.create(title=data["title"], description=data["description"], company=data["company"], location=data["location"],
#                                             posted_by=user, expires_at=data["expires_at"])
#         new_job.save()
#         serializer = self.serializer_class(new_job)
#         return Response(serializer.data)
     
#      def put(self,request, *args, **kwargs):
#         params = kwargs
#         print(params['pk'])
#         data = request.data
#         instance = self.get_object()
#         user = self.request.user
#         update_job = JobPosting.objects.update(instance, title=data["title"], description=data["description"], company=data["company"], location=data["location"],
#                                             posted_by=user, expires_at=data["expires_at"])
        
#         serializer = self.serializer_class(update_job)
#         return Response(serializer.data)



# class JobListView(generics.GenericAPIView, mixins.ListModelMixin):
#      serializer_class = JobPostingSerializer
#      queryset = JobPosting.objects.all()
#      permission_classes = []
#      def get(self, request):
#             return self.list(request)
     
class JobListCreateUpdateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
     serializer_class = JobPostingSerializer
     permission_classes = [IsAuthenticated]
     queryset = JobPosting.objects.all()
     lookup_field = 'id'
     
     def perform_create(self, serializer):
         user = self.request.user
         serializer.save(posted_by=user)
         return super().perform_create(serializer)      
     def get(self, request):
            return self.list(request)    
     def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
     def put(self, request, id=None):
        return self.update(request, id)
   

class UserViewSet(APIView):

    def get(self,request ):
        posts = User.objects.all() 
        serializer = UserSerializer(posts,many=True)
        return Response(serializer.data)
    

class SignupUserView(generics.GenericAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = []
    def post(self, request):
        data = request.data 
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninUserView(APIView):
    permission_classes = []
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})
    def get(self, request):
        content = {"user": str(request.user), 
                   "auth": str(request.auth)}
        
        return Response(data=content, status=status.HTTP_200_OK)

class JobApplicationView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JobApplicationSerializer
    def get_queryset(self):
        jobapplication = JobApplication.objects.all()
        return jobapplication
    
    
    def create(self,request):
        data = request.data
        user = self.request.user
        job_application = JobApplication.objects.create(job_posting=JobPosting.objects.get(id=data["job_posting"]),
                                            applicant=user)
        job_application.save()
        serializer = self.serializer_class(job_application)
        return Response(serializer.data)

class CurrentUserPostsAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class = JobApplicationSerializer 
    queryset = JobApplication.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return JobApplication.objects.filter(applicant=user)
    def get(self, request):
        return self.list(request)
    def delete(self, request, id=None):
        return self.destroy(request, id)



class RegisterView(View):
    form = SignupForm
    def get(self, request):
        form = SignupForm()
        return render(request, 'myapp/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'myapp/signup.html', {'form': form})
    
class LoginView(View):
    form = SigninForm()
    def get(self, request):
        form = SigninForm()
        return render(request, 'myapp/login.html',{"form" : form})
      
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
class Joblist(View):
    def get(self, request):
        jobs=JobPosting.objects.all()
        return render(request,'myapp/index.html',{'jobs':jobs})
class Jobslist(View):
    def get(self, request):
        jobs=JobPosting.objects.all()
        return render(request,'myapp/jobslist.html',{'jobs':jobs})
    
class PublishOfferView(View):
    def post(self,request):
        title = request.POST['title']
        description = request.POST['description']
        company = request.POST['company']
        location = request.POST['location']
        expires_at = request.POST['expireAt']
        user = self.request.user
        
        job = JobPosting(title=title, description=description, company=company, location=location, posted_by= user, expires_at=expires_at)
        job.save()
        return redirect("/")
  
    def get(self, request):
        return render(request, 'myapp/post.html')


class ApplyToOffer(View):
    def get(self, request,id):
        user = self.request.user
        job = JobPosting.objects.get(id=id)
        application = JobApplication(job_posting=job, applicant=user)
        application.save()
        return redirect('myapplication')
    
class CurrentApplication(View):
    def get(self, request):
        user = self.request.user
        apps = JobApplication.objects.filter(applicant=user)
        return render(request,'myapp/application.html',{'apps':apps})
class CurrentApplicationDelete(View):
    def get(self, request, id):
        app = JobApplication.objects.get(id=id)
        app.delete()
        return redirect('myapplication')
