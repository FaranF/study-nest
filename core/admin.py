from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )
    
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__first_name", "user__last_name"]
    list_display = [
        "user_id",
        "first_name",
        "last_name",
        "role",
        "bio",
    ]
    list_editable = ["role"]
    list_per_page = 20
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]
