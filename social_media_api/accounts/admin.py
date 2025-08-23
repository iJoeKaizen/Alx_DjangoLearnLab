# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
    ("Profile", {"fields": ("bio", "profile_picture", "following")}),
    )
    filter_horizontal = ("groups", "user_permissions", "following")



