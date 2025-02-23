from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        print(f'user::{attrs}')
        email_exists = User.objects.filter(email=attrs['email']).exists()
        print(f'user::{email_exists}')
        if email_exists:
            raise serializers.ValidationError("Oooops l'email existe déjà")
        return attrs

    # def create(self, validated_data):
    #     password = validated_data.pop("password")
    #     user = super().create(validated_data)
    #     user.set_password(password)
    #     user.save()
        # Token.objects.create(user=user)
    #     return user
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        Token.objects.create(user=user)
        return user
