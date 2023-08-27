from django.contrib import admin
from .models import Teacher

# Регистрация модели Teacher в админской панели
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'user')
