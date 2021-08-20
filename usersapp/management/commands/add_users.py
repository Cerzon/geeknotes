from django.core.management.base import BaseCommand

from usersapp.models import GeekUser
from usersapp.utils import geek_user_generator


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-c',
            '--count',
            type=int,
            default=5,
            help='Number of users to add',
        )
        parser.add_argument(
            '--super',
            action='store_true',
            help='Create standart GeekBrains superuser',
        )

    def handle(self, *args, **options):
        if options['super']:
            GeekUser.objects.filter(is_superuser=True).delete()
            su = GeekUser.objects.create_superuser(
                username='django',
                email='admin@local.host',
            )
            su.set_password('geekbrains')
            su.save()
        if options['count']:
            user_data = geek_user_generator()
            GeekUser.objects.bulk_create([
                GeekUser(**next(user_data)) for _ in range(options['count'])
            ])
