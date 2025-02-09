from .models import ChatMessage, ChatRoom
from asgiref.sync import sync_to_async
import json
from django.db.models import Q
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from user_app.models import CustomUser


@sync_to_async
def handle_receive_message(
    room_name, username, user_id, message, receiverId, recieverName
):
    room = ChatRoom.objects.get(room_name=room_name)
    user = CustomUser.objects.get(id=user_id)

    if not room.user1 or not room.user2:
        # user_ids = [user_id, receiverId]
        # print("IDS ", user_id, receiverId, user_ids)
        # user_ids.sort()

        receiver = CustomUser.objects.get(id=receiverId)
        if user.id < receiver.id:
            room.user1 = user
            room.user2 = receiver
        else:
            room.user1 = receiver
            room.user2 = user
        room.save()
        print("user1 and user2 is created")

    # user_ids = [user_id, receiverId]
    # print("IDS ", user_id, receiverId, user_ids)
    # user_ids.sort()
    # if room.user1 == user_id:
    #     if username != room.user1_name or recieverName != room.user2_name:
    #         room.user1_name = username
    #         room.user2_name = recieverName
    # else:
    #     if username != room.user2_name or recieverName != room.user1_name:
    #         room.user1_name = recieverName
    #         room.user2_name = username
    # room.save()

    latest_message = ChatMessage.objects.create(
        room_id=room, sender_id=user, content=message
    )
    print("SAVED")

    return room, latest_message


@sync_to_async
def get_chat_messages(room_name):
    messages = ChatMessage.objects.filter(room_id__room_name=room_name).order_by(
        "timestamp"
    )
    return [
        {
            "username": message.sender_id.username,
            "message": message.content,
            "timestamp": message.timestamp.isoformat(),
            "user_id": message.sender_id.id,
        }
        for message in messages
    ]


@database_sync_to_async
def get_chat_rooms(user_id):
    chat_rooms = ChatRoom.objects.filter(Q(user1__id=user_id) | Q(user2__id=user_id))
    print('CHAT LIST user id', user_id)
    for room in chat_rooms:
        print("get_chat_rooms", room.id)
   

    chat_room_with_messages = []
    if chat_rooms:
        for chat_room in chat_rooms:
            latest_message = (
                ChatMessage.objects.filter(room_id=chat_room)
                .order_by("-timestamp")
                .first()
            )
            print('PRINTING IDS')
            print(user_id)
            print(chat_room.user1.id)
            print(chat_room.user2.id)
            user1_id = chat_room.user1.id
            print('TYPE ',type(user_id), type(user1_id))
            if str(user1_id) == str(user_id):
                print('IF case worked')
                chat_room_data = {
                    "id": chat_room.id,
                    "receiver_id": chat_room.user2.id,
                    "receiver_name": chat_room.user2.username,
                    "receiver_picture": chat_room.user2.profile_picture,
                }
            else:
                print('ELSE case worked')
                chat_room_data = {
                    "id": chat_room.id,
                    "receiver_id": chat_room.user1.id,
                    "receiver_name": chat_room.user1.username,
                    "receiver_picture": chat_room.user1.profile_picture,
                }

            message_data = None
            timestamp = None
            if latest_message:
                timestamp = latest_message.timestamp.isoformat()
                message_data = {
                    "id": latest_message.id,
                    "content": latest_message.content,
                    "timestamp": timestamp,
                }

            chat_room_with_messages.append(
                {
                    "room": chat_room_data,
                    "message": message_data,
                    "lates_timestamp": timestamp,
                }
            )

        sorted_chat_rooms = sorted(
            chat_room_with_messages,
            key=lambda X: X["lates_timestamp"] or "",
            reverse=False,
        )
        response_data = [
            {"room": item["room"], "message": item["message"]}
            for item in sorted_chat_rooms
        ]
        print("response_data", response_data)
        return response_data

    return response_data


@sync_to_async
def handle_chat_list(room, latest_message, user_id, receiverId):
    receiver = CustomUser.objects.get(id=receiverId)
    chat_room_data = {
        "id": room.id,
        "receiver_id": receiver.id,
        "receiver_name": receiver.username,
        "receiver_picture": receiver.profile_picture,
    }

    message_data = {
        "id": latest_message.id,
        "content": latest_message.content,
        "timestamp": latest_message.timestamp.isoformat(),
    }

    response_data = {"room": chat_room_data, "message": message_data}
    print('chat list before sending',response_data)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_room_list{user_id}",  # Unique group for the user
        {
            "type": "send_chat_list",
            "chat_list": response_data,
        },
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_room_list{receiverId}",  # Unique group for the user
        {
            "type": "send_chat_list",
            "chat_list": response_data,
        },
    )
