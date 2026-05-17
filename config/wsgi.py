"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Vercel: DATABASE_URL is often only available at runtime, not during build.
_migrate_stamp = Path('/tmp/smart_finance_migrated')
if os.environ.get('DATABASE_URL') and not _migrate_stamp.exists():
    from django.core.management import call_command

    call_command('migrate', '--noinput', verbosity=0)
    _migrate_stamp.touch()
