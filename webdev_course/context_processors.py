from datetime import datetime
from django.conf import settings


def project_version(request):
    return {'project_version': settings.VERSION}

def current_year(request):
    return {'current_year': datetime.now().year}