from django.contrib import admin
from .models import Subject, Task, Submission


# Регистрация модели Subject в админской панели
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')

    # Поле slug будет автоматически заполняться на основе значения поля name
    prepopulated_fields = {"slug": ("name", )}


# Регистрация модели Task в админской панели
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'tests', 'slug')

    # Поле slug будет автоматически заполняться на основе значения поля title
    prepopulated_fields = {"slug": ("title", )}


# Регистрация модели Submission в админской панели
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'task', 'is_correct')
