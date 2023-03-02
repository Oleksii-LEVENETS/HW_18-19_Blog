from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BlogUser, Profile


# Register your models here.
admin.site.register(BlogUser, UserAdmin)
admin.site.register(Profile)
