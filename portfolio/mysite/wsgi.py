"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()

try:
    from django.core.management import call_command
    from portfolyo.seed import ensure_seed_projects

    call_command('migrate', interactive=False, verbosity=0)
    ensure_seed_projects()
except Exception:
    pass
