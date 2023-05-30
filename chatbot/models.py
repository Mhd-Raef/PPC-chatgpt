from django.db import models

class Chat(models.Model):
    context = models.BinaryField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context