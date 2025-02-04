from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserRegisterSerializer
from .utils import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

# IMPORT DATABASE
from .models import CustomUser


# TOKEN GENERATION FUNCTION
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # Custom Claims
    # refresh["username"] = str(user.username)
    # refresh["isAdmin"] = user.is_superadmin

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# class CustomTokenObtainPairView(TokenObtainPairView):
#     # authentication_classes = [] 
#     # permission_classes = [AllowAny]  
#     print('reached in view')
#     serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
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

class LoginView(APIView):
    # authentication_classes = [] 
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = request.data
            print('reached in login')
            serializer = UserSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                user = serializer.validated_data["user"]
                if user.is_active:
                    tokens = get_tokens_for_user(user)
                    print(tokens)

                    # tokens = get_tokens_for_user(user)
                    response_data = {
                        "accessToken": tokens["access"],
                        "refreshToken": tokens["refresh"],
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "profile_picture": user.profile_picture,
                    }
                    response = Response(response_data, status=status.HTTP_200_OK)
                    print('response_data',response_data)
                    return response
                else:
                    return Response(
                        {"Not active": "This account is suspended"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                print(serializer.errors)
                return Response(
                    {"error": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
                
        except Exception as e:
            print(e)
            return Response(
                {'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)

class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            current_user = request.user
            users = CustomUser.objects.exclude(id=current_user.id)
            user_data = [{"id":user.id, "username": user.username, "profile_picture": user.profile_picture} for user in users]

            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            current_user = request.user
            print('current_user',current_user.username)
            user = CustomUser.objects.get(id=user_id)
            user_data = {"id":user.id, "username": user.username, "email": user.email, "profile_picture": user.profile_picture}

            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        