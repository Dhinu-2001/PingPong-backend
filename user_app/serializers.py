from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
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
    def validate_password(self, value):
        """
        Hash the password before storing it in the session.
        """
        return make_password(value)