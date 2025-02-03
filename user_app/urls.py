from django.urls import path
from . import views
from . import utils
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('token/',views.LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('users/', views.UserListView.as_view(), name='users_view'),    
    path('user/<int:user_id>/', views.UserView.as_view(), name='user_view'),    
]