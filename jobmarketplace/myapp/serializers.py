from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User, JobPosting, JobApplication
from rest_framework.authtoken.models import Token
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'username', 'email', 'is_staff', 'is_active']

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'username', 'email', 'password']
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
    

class CurrentUserJobsSerializer(serializers.ModelSerializer):
    job_posting = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ["id", "email", "job_posting"]

class JobPostingSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)

    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'description', 'company', 'location', 'posted_by', 'posted_at', 'expires_at', 'is_active']

class JobApplicationSerializer(serializers.ModelSerializer):
    job_posting = JobPostingSerializer(read_only=True)
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job_posting', 'applicant', 'applied_at', 'status']