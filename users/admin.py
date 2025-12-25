from django.contrib import admin
<<<<<<< HEAD
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
=======

# Register your models here.
>>>>>>> 41ed5fd5187ab39341d77cca20e710c0fa006da1
