from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, username, is_active, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_active=is_active, 
                          is_staff=is_staff, is_superuser=is_superuser, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, username=None, **extra_fields):
        return self._create_user(email, password, username, is_active=True, is_staff=False, 
                                 is_superuser=False, **extra_fields)
    
    def create_superuser(self, email=None, password=None,username=None, **extra_fields):
        return self._create_user(email, password, username, is_active=True, is_staff=True, 
                                 is_superuser=True,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username or self.email.split('@')[0]

