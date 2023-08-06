import os

from subprocess import call

from django.core.files.move import file_move_safe
from django.utils import timezone


from ...settings import (DJANGO_PROJECT_BACKUP_BACKUP_FILE_PREFIX,
                         DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS,
                         DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER,
                         DJANGO_PROJECT_BACKUP_DUMPDATA_JSON_FILENAME,
                         DJANGO_PROJECT_BACKUP_PUBLIC_ASSETS_FOLDERS,
                         DJANGO_PROJECT_BACKUP_PRIVATE_ASSETS_FOLDERS)


def get_backup_name_by_path(path):
    return str(path).split(os.sep)[-1:][0]


# DB

def run_dumpdata_backup():
    excluded_models_string = ' -e '.join(DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS)

    cmd = 'python manage.py dumpdata --indent=4 --natural-foreign {} > {}'.format(excluded_models_string,
                                                                           DJANGO_PROJECT_BACKUP_DUMPDATA_JSON_FILENAME)

    exit_code = call(cmd, shell=True)

    return exit_code


def move_dumpdata_backup(now, compress=False):
    file_path = os.path.abspath(DJANGO_PROJECT_BACKUP_DUMPDATA_JSON_FILENAME)
    file_name = DJANGO_PROJECT_BACKUP_DUMPDATA_JSON_FILENAME

    if not os.path.exists(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER):
        os.mkdir(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER)

    new_file_path = os.path.join(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER, file_name)

    file_move_safe(file_path, new_file_path, allow_overwrite=True)


# assets


def move_assets_backup(file_name):
    file_path = os.path.abspath(os.path.join(file_name))

    if not os.path.exists(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER):
        os.mkdir(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER)

    new_file_path = os.path.join(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER, file_name)

    file_move_safe(file_path, new_file_path, allow_overwrite=True)


def run_public_assets_backup(now):
    for folder in DJANGO_PROJECT_BACKUP_PUBLIC_ASSETS_FOLDERS:
        public_backup_filename = '{}.{}.public.gz'.format(DJANGO_PROJECT_BACKUP_BACKUP_FILE_PREFIX, now)

        cmd = 'tar --exclude="{2}{0}media{0}filer_public_thumbnails" --exclude="{2}{0}static" -cvjf {1} {2}'.format(
            os.path.sep,
            public_backup_filename,
            os.path.abspath(folder))

        exit_code = call(cmd, shell=True)

        if exit_code == 0:
            move_assets_backup(public_backup_filename)

        return exit_code


def run_private_assets_backup(now):
    for folder in DJANGO_PROJECT_BACKUP_PRIVATE_ASSETS_FOLDERS:
        private_backup_filename = '{}.{}.private.gz'.format(DJANGO_PROJECT_BACKUP_BACKUP_FILE_PREFIX, now)

        cmd = 'tar -cvjf {1} {2}'.format(
            os.path.sep,
            private_backup_filename,
            os.path.abspath(folder))

        exit_code = call(cmd, shell=True)

        if exit_code == 0:
            move_assets_backup(private_backup_filename)

        return exit_code
