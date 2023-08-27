from django.urls import path
from .views import (
    IndexView,
    FeedbackPopupView
)


app_name = 'core'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('feedback', FeedbackPopupView.as_view(), name='feedback')
]
