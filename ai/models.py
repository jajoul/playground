from django.db import models

# Create your models here.
class AiChat(models.Model):
    first_bot_name=models.CharField(max_length=100)
    second_bot_name=models.CharField(max_length=100)
    subject=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering=['-created_at']
        verbose_name_plural='AiChats'
        verbose_name='AiChat'

class ChatMessage(models.Model):
    aichat = models.ForeignKey(AiChat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.role}: {self.content[:50]}'
    
    class Meta:
        ordering=['created_at']
        verbose_name_plural='Chat Messages'
        verbose_name='Chat Message'