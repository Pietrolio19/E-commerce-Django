from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    CAP = models.IntegerField(default=0)
    is_store_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.username