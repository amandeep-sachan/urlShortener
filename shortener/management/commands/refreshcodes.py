from django.core.management.base import BaseCommand,CommandError

from shortener.models import DjangoURL

class Command(BaseCommand):
    help = 'Refreshes all DjangoURL shortcodes.'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)
        parser.add_argument

    def handle(self, *args, **options):
        return DjangoURL.objects.refresh_shortcodes(items=options['items'])