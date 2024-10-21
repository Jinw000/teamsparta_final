"""
WSGI config for gpting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpting.settings')

application = get_wsgi_application()

# 경로 추가
sys.path.append('/home/ubuntu/gpting')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpting.settings')
application = get_wsgi_application()