from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from .utils import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    authentication_classes = []  # ✅ Disable authentication checks for login
    permission_classes = [AllowAny]  # ✅ Allow anyone to access login
    print('reached in view')
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    authentication_classes = []  # ✅ Disable authentication checks for this view
    permission_classes = [AllowAny]  # ✅ Allow anyone to access registration
    
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {'message':'Successfully registered'}, status=status.HTTP_201_CREATED
                )
            else:
                error_messages = []
                for field, errors in serializer.errors.items():
                    for error in errors:
                        if field == "email" and "unique" in error:
                            error_messages.append("Email already exists")
                        else:
                            error_messages.append(f"{field.capitalize()}: {error}")

            content = {"error": error_messages}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)
