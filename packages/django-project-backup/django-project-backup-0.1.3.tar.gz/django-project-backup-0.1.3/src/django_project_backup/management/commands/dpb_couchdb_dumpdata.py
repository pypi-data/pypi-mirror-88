from django.core.management.base import BaseCommand

from ...utils.couchdb import dumpdata


class Command(BaseCommand):
    help = 'Performs complete dumpdata to couchdb instance.'

    def handle(self, *args, **options):
        try:
            ids_to_send, sent_ids, ids_to_delete, deleted_ids = dumpdata()

            self.stdout.write(self.style.SUCCESS('Sent: {}/{}, Deleted: {}/{}'.format(len(ids_to_send),
                                                                                      len(sent_ids),
                                                                                      len(ids_to_delete),
                                                                                      len(deleted_ids))))

        except Exception as e:
            self.stdout.write(self.style.ERROR('Error "{}"'.format(e)))
            raise

        else:
            self.stdout.write(self.style.SUCCESS('Done'))
