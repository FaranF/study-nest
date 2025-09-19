from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_INSTRUCTOR = "I"
    ROLE_STUDENT = "S"
    ROLE_CHOICES = [
        (ROLE_INSTRUCTOR, "Instructor"),
        (ROLE_STUDENT, "Student"),
    ]

    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]

