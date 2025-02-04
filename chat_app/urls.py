from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_id>/', views.UserChatView.as_view(), name="user_chat_view"),
    path('send-interest/', views.InterestView.as_view(), name="interest_view"),
    path('decision-interest/', views.DecisionInterestView.as_view(), name="decision_interest_view"),
]