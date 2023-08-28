from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    AuthSelectView,
    IndexView,
    FeedbackPopupView
)


app_name = 'core'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('auth_select/', AuthSelectView.as_view(), name='auth_select'),
    path('feedback', FeedbackPopupView.as_view(), name='feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)