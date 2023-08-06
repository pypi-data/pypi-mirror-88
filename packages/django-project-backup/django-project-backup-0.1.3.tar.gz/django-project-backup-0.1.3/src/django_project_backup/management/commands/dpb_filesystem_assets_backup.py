from django.core.management.base import BaseCommand  # , CommandError
from django.utils import timezone

from ...utils.filesystem import run_private_assets_backup, run_public_assets_backup
from ...settings import DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER


class Command(BaseCommand):
    help = 'Performs assets TAR+BZIP2 file backup'

    #def add_arguments(self, parser):
    #    parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        now = timezone.now().strftime('%Y_%m_%dT%H_%M')

        try:
            exit_code_1 = run_public_assets_backup(now)
            if exit_code_1 != 0:
                self.stdout.write(self.style.ERROR('Wrong exit code running public assets backup ({})'.format(exit_code_1)))
                return

            else:
                exit_code_2 = run_private_assets_backup(now)
                if exit_code_2 != 0:
                    self.stdout.write(
                        self.style.ERROR('Wrong exit code running private assets backup ({})'.format(exit_code_2)))
                    return

            self.stdout.write(
                self.style.SUCCESS('Assets backup done into "{}"'.format(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER)))

        except Exception as e:
            self.stdout.write(self.style.ERROR('Error executing assets backup: {}'.format(e)))
            raise
