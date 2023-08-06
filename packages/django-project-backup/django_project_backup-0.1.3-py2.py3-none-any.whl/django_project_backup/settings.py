import os

from django.conf import settings


_DJANGO_PROJECT_BACKUP_SHAPES = ('manual', 'realtime')
DJANGO_PROJECT_BACKUP_SHAPE = getattr(settings, 'DJANGO_PROJECT_BACKUP_SHAPE', _DJANGO_PROJECT_BACKUP_SHAPES[0])

_DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS = [
    # 'migrations',
    'auth.permission',
    'contenttypes',
]
DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS = _DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS + \
                                        getattr(settings, 'DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS', [
                                                    'sessions',
                                                    'admin'
                                                ])

COUCHDB_DATASTORE_HOST = getattr(settings, 'COUCHDB_DATASTORE_HOST', 'http://127.0.0.1:5984')
COUCHDB_DATASTORE_USER = getattr(settings, 'COUCHDB_DATASTORE_USER', 'admin')
COUCHDB_DATASTORE_PASSWORD = getattr(settings, 'COUCHDB_DATASTORE_PASSWORD', 'couchdb')
# couchdb db index
COUCHDB_DATASTORE_DATABASE_NAME = getattr(settings, 'COUCHDB_DATASTORE_DATABASE_NAME', 'django_project_backup')


_PUBLIC_ASSETS_FOLDERS = [
    settings.PUBLIC_ROOT,
]

_PRIVATE_ASSETS_FOLDERS = [
    settings.PRIVATE_ROOT,
]

DJANGO_PROJECT_BACKUP_DUMPDATA_JSON_FILENAME = 'dump_all.json'
DJANGO_PROJECT_BACKUP_BACKUP_FILE_PREFIX = 'backup'

DJANGO_PROJECT_BACKUP_PUBLIC_ASSETS_FOLDERS = getattr(settings, 'DJANGO_PROJECT_BACKUP_PUBLIC_ASSETS_FOLDERS',
                                                      _PUBLIC_ASSETS_FOLDERS)

DJANGO_PROJECT_BACKUP_PRIVATE_ASSETS_FOLDERS = getattr(settings, 'DJANGO_PROJECT_BACKUP_PRIVATE_ASSETS_FOLDERS',
                                                       _PRIVATE_ASSETS_FOLDERS)

_BACKUP_DESTINATION_FOLDER = os.path.abspath('.{}backups'.format(os.path.sep))

DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER = getattr(settings, 'DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER',
                                                   _BACKUP_DESTINATION_FOLDER)
