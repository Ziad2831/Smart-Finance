"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()


def _migration_database_configured():
    for key in (
        'POSTGRES_URL_NON_POOLING',
        'DATABASE_URL',
        'POSTGRES_URL',
        'NEON_DATABASE_URL',
    ):
        if os.environ.get(key):
            return True
    return False


_migrate_stamp = Path('/tmp/smart_finance_migrated')
if os.environ.get('VERCEL') and not _migrate_stamp.exists():
    from django.core.management import call_command

    try:
        call_command('migrate', '--noinput', verbosity=1)
        _migrate_stamp.touch()
    except Exception as exc:
        print(f'[smart-finance] migrate failed: {exc}', file=sys.stderr)
