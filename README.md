# Проект: e-Learning

Проект E-learning представляет собой платформу для обучения с возможностью взаимодействия между преподавателями и студентами.

## Приложения
- **core**
  для основных страниц сайта (для не авторизированных пользователей), 404
- **students**
  для авторизации студента и страниц контента для студентов
- **teachers**
  для авторизации преподавателя и страниц контента для преподавателей

## Установка проекта
1. Клонировать репозиторий
`git clone https://github.com/Eldar-Kadymov/webdev-course.git`

2. Перейти в директорию проекта
`cd webdev_course`


## Запуск проекта
Установить virtualenv (Если не установлено)
`pip install virtualenv`

1. Создать виртуальное окружение
`virtualenv venv`
2. Активировать виртуальное окружение
  - Windows
    `venv\Scripts\activate`
  - Linux/macOS
    `source venv/bin/activate`
3. Установить зависимости
`pip install -r requirements.txt`
4. Запуск проекта
`python manage.py runserver`
5. Завершение работы в виртуальном окружении
`deactivate`