from main.tasks import check_time_field
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    help = 'Load subtitles from server django'

    def handle(self, *args, **kwargs):
        data  = check_time_field()

        self.stdout.write(f"{data}")

   