from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from user_app.models import CustomUser
from .models import ChatRoom, Interests
from notification_app.utils import send_user_notification
from asgiref.sync import sync_to_async
# Create your views here.


class UserChatView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            print("reached", user_id)

            try:
                user = CustomUser.objects.get(id=user_id)
                print(user)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_200_OK)

            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_picture": user.profile_picture,
            }

            sender = request.user.id
            receiver = user_id
            sorted_arr = sorted([sender, receiver])
            room_name = f"chat_{sorted_arr[0]}-{sorted_arr[1]}"
            print(room_name)

            response = {}  # ✅ Ensure response is always initialized

            try:
                room_obj = ChatRoom.objects.get(room_name=room_name)
                chat_room_status = "exist"

                response = {
                    "user_data": user_data,
                    "chat_room": room_obj.room_name,
                    "chat_room_status": chat_room_status,
                }
            except ChatRoom.DoesNotExist:
                try:
                    print("room name", room_name)
                    interest_obj = Interests.objects.get(room_name=room_name)

                    if interest_obj.recipient_id.id == request.user.id:
                        chat_room_status = "Decision"
                    elif interest_obj.sender_id.id == request.user.id:
                        chat_room_status = "Pending"
                    else:
                        chat_room_status = "not exist"

                    response = {
                        "user_data": user_data,
                        "chat_room_status": chat_room_status,
                    }
                except Interests.DoesNotExist:
                    print("interest_obj DoesNotExist")
                    chat_room_status = "not exist"
                    response = {
                        "user_data": user_data,
                        "chat_room_status": chat_room_status,
                    }

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InterestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            print("data", data)
            
            sender_id = CustomUser.objects.get(id=data.get("senderId"))
            receiverId = CustomUser.objects.get(id=data.get("receiverId"))

            interest_obj, create = Interests.objects.get_or_create(
                room_name=data.get("roomName"),
                sender_id=sender_id,
                recipient_id=receiverId,
                status=data.get("status"),
            )
            
            # SENDING NOTIFICAITON
            notification_message = f"{sender_id.username} sent you an interest request"
            type = 'New Interest'
            print('notification_message',notification_message)

            send_user_notification(receiverId.id, notification_message, type, senderId=sender_id.id)    #NOT NEEDED
        
            return Response(
                {"message": "interest_created"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DecisionInterestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            print(data)
            try:
                interests_obj = Interests.objects.get(room_name=data.get("roomName"))
                if data["decision"] == "Accepted":
                    chatroom_obj = ChatRoom.objects.create(room_name=data["roomName"])
                    interests_obj.delete()
                elif data["decision"] == "Declined":
                    interests_obj.delete()
                return Response(
                    {
                        "message": f'{data["decision"]} the interest request successfully.'
                    },
                    status=status.HTTP_200_OK,
                )
            except Interests.DoesNotExist:
                return Response(
                    {"error": "Interest request not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            print(e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
