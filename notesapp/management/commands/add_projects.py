from random import choices, randint
from django.core.management.base import BaseCommand

from notesapp.models import Project
from usersapp.models import GeekUser


NAMES = ('Amphitruo', 'Asinaria', 'Miles gloriosus', 'Mostellaria', 'Captivi',
    'Cistellaria', 'Curculio', 'Epidicus', 'Trinummus', 'Truculentus',
    'Mercator', 'Pseudolus', 'Poenulus')


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-c',
            '--count',
            type=int,
            default=5,
            help='Number of projects to add',
        )

    def handle(self, *args, **options):
        if options['count']:
            Project.objects.bulk_create([
                Project(name=' '.join(choices(NAMES, k=randint(1, 4))).capitalize())
                for _ in range(options['count'])
            ])
            for project in Project.objects.all():
                for user in GeekUser.objects.exclude(is_superuser=True).order_by('?')[:randint(1, 5)]:
                    project.users.add(user)
