from django.core.management.base import BaseCommand

from ...utils.couchdb import loaddata


class Command(BaseCommand):
    help = 'Performs complete loaddata from couchdb instance.'

    def handle(self, *args, **options):
        try:
            loaded_ids = loaddata()

            self.stdout.write(self.style.SUCCESS('Loaded: {}'.format(loaded_ids)))

        except Exception as e:
            self.stdout.write(self.style.ERROR('Error "{}"'.format(e)))
            raise

        else:
            self.stdout.write(self.style.SUCCESS('Done'))
