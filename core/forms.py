from django import forms
from .models import Feedback, Task

class SubmissionForm(forms.Form):
    code = forms.CharField()


class TestForm(forms.Form):
    input = forms.IntegerField()
    output = forms.IntegerField()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'message']
        labels = {
            'name': 'Тема',
            'message': 'Описание проблемы'
        }