from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "profile_picture", "password"]
        
    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data['username'],
                                         email=validated_data['email'],
                                        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    # username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser   # Specify the model you're working with
        fields = ['email', 'password']  # Define the fields you want to include
    def validate(self, data):
        email = data.get('email').strip()
        password = data.get('password').strip()
        if not email or not password:
            raise serializers.ValidationError('Both username and password are required')
        user = authenticate(email=email, password=password)

        if user is None:
            print('user isn none', user)
            raise serializers.ValidationError('Invalid username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is inactive')

        data['user'] = user
        return data