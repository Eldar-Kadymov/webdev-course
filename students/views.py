import json
import subprocess

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.views import View

from core.models import Subject, Task, Submission
from .forms import LoginForm
from core.forms import SubmissionForm
from .decorators import student_required


class LoginView(View):
    template_name: str = 'students/login.html'

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
                    if hasattr(user, 'student'):
                        return redirect('students:subject_list')
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
        return redirect('students:login')


class SubjectListView(View):
    template_name = 'students/subject_list.html'

    @method_decorator(student_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        subjects = Subject.objects.all()
        student = request.user.student
        subject_data = []
        for subject in subjects:
            tasks_in_subject = Task.objects.filter(subject=subject)
            completed_tasks = Submission.objects.filter(task__in=tasks_in_subject, student=student, is_correct=True).count()
            total_tasks = tasks_in_subject.count()
            if total_tasks > 0:
                completion_percentage = int((completed_tasks / total_tasks) * 100)
            else:
                completion_percentage = 0
            subject_data.append({'subject': subject, 'completion_percentage': completion_percentage})

        context = {'subject_data': subject_data, 'student': student}
        return render(request, self.template_name, context)


class TaskListView(View):
    template_name: str = 'students/task_list.html'

    @method_decorator(student_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, subject_slug: str, *args, **kwargs) -> HttpResponse:
        subject = get_object_or_404(Subject, slug=subject_slug)
        tasks = Task.objects.filter(subject=subject)
        student = request.user.student
        context = {'subject': subject, 'student': student, 'tasks': tasks}
        return render(request, self.template_name, context)


class SubmitSolutionView(View):
    template_name: str = 'students/submit_solution.html'

    @method_decorator(student_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, task_slug: str, *args, **kwargs) -> HttpResponse:
        task = get_object_or_404(Task, slug=task_slug)
        student = request.user.student
        last_submission = student.submission_set.filter(task=task).last()

        initial_data: dict = {}
        if last_submission:
            initial_data['code'] = last_submission.code

        form = SubmissionForm(initial=initial_data)
        context = {'student': student, 'form': form, 'task': task}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, task_slug: str, *args, **kwargs) -> HttpResponse:
        task = get_object_or_404(Task, slug=task_slug)
        student = request.user.student

        form = SubmissionForm(request.POST)
        if form.is_valid():
            student_code = form.cleaned_data['code']

            test_results = self.run_tests(task, student_code)
            is_passed = all(result['status'] ==
                            'passed' for result in test_results)

            submission, created = Submission.objects.get_or_create(
                task=task, student=student)
            submission.code = student_code
            submission.result = test_results
            submission.is_correct = is_passed
            submission.save()

            result_context = {
                'student': student,
                'task': task,
                'is_passed': is_passed,
                'test_results': test_results
            }
            return render(request, 'students/result.html', result_context)

        context = {'student': student, 'form': form, 'task': task}
        return render(request, self.template_name, context)

    def run_tests(self, task: Task, student_code: str) -> 'list[dict]':
        test_results = []
        try:
            tests = json.loads(task.tests)

            for test in tests:
                # Извлечение входных данных из тестового случая
                input_data = test['input']

                # Создание подпроцесса для выполнения кода студента
                process = subprocess.Popen(
                    ['python', '-c', student_code],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8'
                )
                # Общение с подпроцессом, передача входных данных и установка времени ожидания
                stdout, stderr = process.communicate(
                    input=input_data, timeout=5)

                # Извлечение фактического вывода из стандартного вывода подпроцесса
                actual_output = stdout.strip()

                expected_output = test['output']
                if actual_output == expected_output:
                    test_result = {'status': 'passed'}
                else:
                    test_result = {
                        'status': 'failed',
                        'expected_output': expected_output,
                        'actual_output': actual_output,
                        'error_message': ''
                    }

                test_results.append(test_result)
        except subprocess.TimeoutExpired:
            # превышение времени выполнения при запуске кода
            test_results.append(
                {'status': 'failed', 'error_message': 'Timeout'})

        return test_results
