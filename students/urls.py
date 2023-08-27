from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    LoginView,
    LogoutView,
    SubjectListView,
    TaskListView,
    SubmitSolutionView
)


app_name = 'students'  # Пространство имен для приложения

# Настройка маршрутов (URL-шаблонов)
urlpatterns = [
    # Маршрут для страницы входа
    path('login/',
         LoginView.as_view(), name='login'),

    # Маршрут для страницы выхода
    path('logout/',
         LogoutView.as_view(), name='logout'),

    # Маршрут для списка предметов
    path('subjects/',
         SubjectListView.as_view(), name='subject_list'),

    # Маршрут для списка задач по конкретному предмету
    path('subjects/<slug:subject_slug>/',
         TaskListView.as_view(), name='task_list'),

    # Маршрут для страницы отправки решения задачи
    path('tasks/<slug:task_slug>/',
         SubmitSolutionView.as_view(), name='submit_solution'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
