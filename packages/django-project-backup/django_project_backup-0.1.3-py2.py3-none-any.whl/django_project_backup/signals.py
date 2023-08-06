import logging

from django.db.models.signals import post_save, post_delete, m2m_changed

from .settings import DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS

logger = logging.getLogger(__name__)


def update_model(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        app_label = instance._meta.app_label

        if app_label not in DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS and not app_label.startswith('migration'):
            if created:
                print('create_model', app_label, sender, instance, kwargs)
            else:
                print('update_model', app_label, sender, instance, kwargs)


def delete_model(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        app_label = instance._meta.app_label

        if app_label not in DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS:
            print('delete_model', app_label, sender, instance, kwargs)


def update_model_relations(sender, instance, action, **kwargs):
    if not kwargs.get('raw', False):
        if action == 'post_remove':
            app_label = instance._meta.app_label

            if app_label not in DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS:
                print('update_model_relations', app_label, action, sender, instance, kwargs)


post_save.connect(update_model)
post_delete.connect(delete_model)
m2m_changed.connect(update_model_relations)
