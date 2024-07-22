"""
ASGI config for gpt_engineer_enhanced_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from asgiref.compatibility import guarantee_single_callable


from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpt_engineer_enhanced_web.settings")

application = get_asgi_application()
application = guarantee_single_callable(application)
