from django.contrib import admin
from .models import User, JobApplication, JobPosting
# Register your models here.

admin.site.register(User)
admin.site.register(JobApplication)
admin.site.register(JobPosting)