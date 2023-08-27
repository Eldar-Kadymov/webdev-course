from django.db import models
from django.contrib.auth.models import User


# Добавляем свойство "is_student" к модели User
User.add_to_class('is_student', property(
    lambda self: hasattr(self, 'student')))


class Student(models.Model):
    # Связь для представления студента как пользователя
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,  related_name='student')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    avatar = models.ImageField(
        upload_to='profile_photos/',  # Путь для сохранения аватаров
        null=True,  # Разрешаем значение NULL
        blank=True,  # Разрешаем пустое значение
        # Путь к значению по умолчанию
        default='profile_photos/{}.png'.format('Smiling-Penguin')
    )

    def __str__(self):
        return self.get_full_name()

    # Получение полного имени студента
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    # Проверка, является ли пользователь студентом
    @property
    def is_student(self) -> bool:
        return True
