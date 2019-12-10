from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager

class UserManager(BaseUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(nickname="", phone="", *args, **kwargs)

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.username