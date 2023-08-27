from django.db import models
from django.contrib.auth.models import User

from students.models import Student


class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField()
    tests = models.TextField()  # JSON-подобный формат для хранения тестов
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"{self.subject} - Task {self.id}"
    
# Пример JSON-тестов для задания
# [
#     {
#         "input": {"a": 2, "b": 3},
#         "output": 5
#     },
#     ...
# ]
    

class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    code = models.TextField()
    result = models.TextField()  # JSON-подобный формат для хранения результатов
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.task}"
    
# Пример JSON-результатов для отправленного решения
# [
#     {"status": "passed"},
#     {"status": "failed", "expected_output": 4, "actual_output": "5", "error_message": ""},
#     ...
# ]


class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name