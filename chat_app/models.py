from django.db import models
from user_app.models import CustomUser

# Create your models here.

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='room_user1', null=True, blank=True)
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='room_user2', null=True, blank=True)

    def __str__(self):
        return self.room_name
    
class ChatMessage(models.Model):
    room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_sender')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content[:20]}"

class Interests(models.Model):
    room_name = models.CharField(max_length=255, unique=True, default='null')
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interest_sender')
    recipient_id  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interest_recipient')
    status = models.CharField(max_length=50, choices=[('Pending', 'pending'), ('Accepted', 'accepted'), ('Declined', 'declined')], default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name
    