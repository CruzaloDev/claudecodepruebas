"""
ASGI config for fulfillment project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fulfillment.settings')

application = get_asgi_application()
