from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from typing import Callable


def student_required(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # Проверяем, аутентифицирован ли пользователь и является ли он студентом
        if not request.user.is_authenticated or not request.user.is_student:
            return redirect(reverse('students:login'))

        return view_func(request, *args, **kwargs)


    return _wrapped_view
