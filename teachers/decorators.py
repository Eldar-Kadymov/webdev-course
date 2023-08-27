from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from typing import Callable


def teacher_required(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # Проверяем, аутентифицирован ли пользователь и является ли он преподавателем
        if not request.user.is_authenticated or not request.user.is_teacher:
            return redirect(reverse('teachers:login'))

        return view_func(request, *args, **kwargs)


    return _wrapped_view
