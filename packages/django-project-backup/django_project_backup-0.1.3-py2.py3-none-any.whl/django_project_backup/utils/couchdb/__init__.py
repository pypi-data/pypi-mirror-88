from django.core.management.commands import (dumpdata as _dumpdata,
                                             loaddata as _loaddata)
from django.core.management import call_command

from unittest.mock import patch

from ...settings import DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS
from .adapter import DBAdapter
from .stream import CouchdbStream


@patch('sys.argv', ['./manage.py', 'dumpdata'])  # https://github.com/django-polymorphic/django-polymorphic/issues/146
def dumpdata():
    """
    Command line equivalent:

    python manage.py dumpdata --natural-foreign \
        -e auth.permission -e contenttypes -e sessions -e admin ... > dump_file.json
    """

    cmd = _dumpdata.Command()
    stream = CouchdbStream()

    try:
        # get remote ids
        remote_ids = stream.db.get_documents_ids()

        # dump to FS
        options = {
            'format': 'couchdb_datastore',
            'exclude': DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS,
            'output': stream.get_output_name(),
            'use_natural_foreign_keys': True,
            'verbosity': 0
        }
        call_command(cmd, **options)

        # send to couchdb
        stream.send()
        sent_ids = stream.sent_ids
        ids_to_send = sent_ids

        # calculate and remove deleted models ids
        ids_to_delete = [item for item in remote_ids if item not in sent_ids]
        deleted_ids = [stream.db.delete_document(key) for key in ids_to_delete]

    except:
        raise

    else:
        del stream

    return ids_to_send, sent_ids, ids_to_delete, deleted_ids


@patch('sys.argv', ['./manage.py', 'loaddata'])
def loaddata():
    """
    Command line equivalent:

        python manage.py loaddata dump_file.json
    """
    cmd = _loaddata.Command()
    stream = CouchdbStream()

    options = {
        'exclude': DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS,
        'verbosity': 0
    }

    try:
        stream.retrieve()
        loaded_ids = stream.loaded_ids

        file_path = stream.get_output_name()

        call_command(cmd, file_path, **options)

    except:
        raise

    else:
        del stream

    return loaded_ids
