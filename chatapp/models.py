from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(unique=True)

  def __str__(self):
    return self.name
  
class ChatMessage(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
  message_contant = models.TextField()
  date = models.DateTimeField(auto_now=True)

  class Meta:
    ordering=('date',)

  def __str__(self):
    return f'{self.user.username} | {self.room.name}'
  

  