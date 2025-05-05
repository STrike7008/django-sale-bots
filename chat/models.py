from django.db import models

class Message(models.Model):
    user_name = models.CharField(max_length=255)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_name}: {self.message_text}'

    class Meta:
        verbose_name = "Повідомлення"
        verbose_name_plural = "Повідомлення"