from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print('reached')
        username = attrs.get("username")
        password = attrs.get("password")

        print("Trying to authenticate:", username, password)  # ✅ Debug

        # user = authenticate(username=username, password=password)
        # print("user", user)

        # if user is None:
        #     print("Authentication failed!")  # ✅ Debug
        #     raise serializers.ValidationError({"error": "Invalid username or password"})
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed({"error": "Invalid username or password"})
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["profile_picture"] = self.user.profile_picture
        return data
