from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

from django.urls import reverse


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    slug = models.SlugField(max_length=255, blank=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.uuid)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.username


class Gender(models.Model):
    gender = models.CharField(max_length=1, unique=True)
    
    def __str__(self) -> str:
        return self.gender


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    slug = models.SlugField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    other_names = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.uuid)
        super().save(*args, **kwargs)
    
    def get_user_email(self):
        return self.user.email

    def __str__(self) -> str:
        return self.user.username
