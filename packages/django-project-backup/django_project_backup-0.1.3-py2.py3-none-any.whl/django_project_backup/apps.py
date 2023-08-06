from django.apps import AppConfig


class DjangoProjectBackupConfig(AppConfig):
    name = 'django_project_backup'
    verbose_name = 'Django Project Backup'

    def ready(self):
        from .settings import DJANGO_PROJECT_BACKUP_SHAPE

        if DJANGO_PROJECT_BACKUP_SHAPE == 'realtime':
            try:
                from . import signals  # noqa F401

            except ImportError:
                pass
