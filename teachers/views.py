import json
from slugify import slugify

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

from core.models import Subject, Task, Submission
from students.models import Student
from .forms import LoginForm
from core.forms import TaskForm
from .decorators import teacher_required


class LoginView(View):
    template_name: str = 'teachers/login.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = LoginForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            with transaction.atomic():
                user = authenticate(
                    request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    if hasattr(user, 'teacher'):
                        return redirect('teachers:subject_list')
                    else:
                        # Если не существует
                        pass
                else:
                    form.add_error(
                        None, 'Неверное имя пользователя или пароль.')

        context = {'form': form}
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        # После выхода из учетной записи студента перенаправляем на страницу авторизации
        return redirect('teachers:login')


class SubjectListView(View):
    template_name = 'teachers/subject_list.html'

    @method_decorator(teacher_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        subjects = Subject.objects.all()
        context = {'subjects': subjects}
        return render(request, self.template_name, context)


class SubjectStatisticsView(View):
    template_name: str = 'teachers/subject_statistics.html'

    @method_decorator(teacher_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, subject_slug: str, *args, **kwargs) -> HttpResponse:
        subject = Subject.objects.get(slug=subject_slug)
        students = Student.objects.all()
        tasks = subject.task_set.all()

        search_student = request.GET.get('search_student', '')

        student_statistics = {}

        for student in students:
            if search_student and search_student.lower() not in student.get_full_name().lower():
                continue

            student_stats = []

            for task in tasks:
                submission = Submission.objects.filter(
                    task=task,
                    student=student
                ).first()

                student_stats.append(submission.id if submission else None)

            student_statistics[student] = student_stats

        context = {
            'subject': subject,
            'student_statistics': student_statistics,
            'tasks': tasks,
            'search_student': search_student,
        }
        return render(request, self.template_name, context)


class ViewSubmissionView(View):
    template_name = 'teachers/view_submission.html'

    @method_decorator(teacher_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, submission_id: int, *args, **kwargs) -> HttpResponse:
        submission = get_object_or_404(Submission, pk=submission_id)
        context = {'submission': submission}
        return render(request, self.template_name, context)


class TaskListView(View):
    template_name: str = 'teachers/task_list.html'

    @method_decorator(teacher_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, subject_slug: str, *args, **kwargs) -> HttpResponse:
        subject = get_object_or_404(Subject, slug=subject_slug)
        tasks = Task.objects.filter(subject=subject)
        context = {'subject': subject, 'tasks': tasks}
        return render(request, self.template_name, context)


class TaskDetailView(View):
    template_name: str = 'teachers/task_detail.html'

    @method_decorator(teacher_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, task_slug: str, *args, **kwargs) -> HttpResponse:
        task = get_object_or_404(Task, slug=task_slug)
        tests = json.loads(task.tests)
        context = {'task': task, 'tests': tests}
        return render(request, self.template_name, context)


class CreateTaskView(View):
    template_name = 'teachers/task_add.html'

    @method_decorator(teacher_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, subject_slug: str, *args, **kwargs) -> HttpResponse:
        subject = get_object_or_404(Subject, slug=subject_slug)
        form = TaskForm()
        context = {'form': form, 'subject': subject}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, subject_slug: str, *args, **kwargs) -> HttpResponse:
        subject = get_object_or_404(Subject, slug=subject_slug)
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.subject = subject
            # Генерация slug на основе названия задачи
            task.slug = slugify(task.title)
            tests = []

            # Проходимся по всем тестам, указанным в POST-запросе
            for i in range(int(request.POST['test_count'])):
                input_data = request.POST[f'input_{i}']  # Получаем входные данные для теста
                output_data = request.POST[f'output_{i}']  # Получаем ожидаемый результат для теста
                tests.append({'input': input_data, 'output': output_data})  # Добавляем тест в список

            task.tests = json.dumps(tests, ensure_ascii=False)
            task.save()

        context = {'form': form, 'subject': subject}
        return render(request, self.template_name, context)
