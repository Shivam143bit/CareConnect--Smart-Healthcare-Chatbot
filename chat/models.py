from django.db import models

# Create your models here.
class ChatSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, default="New medical chat")

class Message(models.Model):
    ROLE_CHOICES = [("user","user"), ("assistant","assistant"), ("system","system")]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)