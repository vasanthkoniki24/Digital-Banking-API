from django.db import models

class UserData(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    balance = models.FloatField(default=1000)

class Transaction(models.Model):
    sender = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='received')
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
