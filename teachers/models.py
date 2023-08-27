from django.db import models
from django.contrib.auth.models import User


# Добавляем новое свойство "is_teacher" к модели User
User.add_to_class('is_teacher', property(
    lambda self: hasattr(self, 'teacher')))


class Teacher(models.Model):
    # Связь для представления учителя как пользователя
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='teacher')

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.get_full_name()

    # Получение полного имени преподавателя
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    # Проверка, является ли пользователь учителем
    @property
    def is_teacher(self) -> bool:
        return True
