from django.contrib import admin
from .models import Student


# Регистрация модели Student в админской панели
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'email')
