from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    SubjectListView,
    SubjectStatisticsView,
    TaskListView,
    TaskDetailView,
    ViewSubmissionView,
    CreateTaskView
)


app_name = 'teachers'  # Пространство имен для приложения учителей

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

    # Маршрут для статистики по предмету
    path('subject/<slug:subject_slug>/',
         SubjectStatisticsView.as_view(), name='subject_statistics'),

    # Маршрут для списка задач по предмету
    path('subject/<slug:subject_slug>/tasks/',
         TaskListView.as_view(), name='task_list'),

    # Маршрут для просмотра конкретного решения
    path('submission/<int:submission_id>/',
         ViewSubmissionView.as_view(), name='view_submission'),

    # Маршрут для описания задания
    path('task/<slug:task_slug>/',
         TaskDetailView.as_view(), name='task_detail'),

    # Маршрут для создания нового задания
    path('subjects/<slug:subject_slug>/create_task/',
         CreateTaskView.as_view(), name='task_add'),
]
