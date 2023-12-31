
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('students/', include('students.urls', namespace='students')),
    path('teachers/', include('teachers.urls', namespace='teachers')),

    # Административная панель Django
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)