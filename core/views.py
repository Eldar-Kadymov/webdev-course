from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse

from .forms import FeedbackForm


class IndexView(View):
    def get(self, request):
        return render(request, 'core/index.html')
    
class AuthSelectView(View):
    def get(self, request):
        return render(request, 'core/auth_select.html')

class FeedbackPopupView(View):
    template_name = 'core/feedback.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = FeedbackForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sender = request.user if request.user.is_authenticated else None
            form.save()

            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            # Верните ошибки формы в формате JSON
            errors = form.errors.as_json()
            return HttpResponse(errors, content_type='application/json', status=400)