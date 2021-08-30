from random import choices, randint
from django.core.management.base import BaseCommand

from notesapp.models import Project, Note


TEXT = """Alea jacta est.
Amicus cognoscitur amore, more, ore, re.
Aqua cavat lapidem non vi, sed saepe cadendo.
Asinus asinorum in saecula saeculorum.
Barba crescit caput nescit.
Bellum omnium contra omnes.
Bona fama divitiis est potior.
Carum est quod rarum est.
Charta non erubescit.
Chorus magno cursum rapit effera.
Concordia parvae res crescunt, discordia maximae dilabuntur.
Consuetudo altera natura.
Debes ergo potes.
Deus ex machina.
Dictum est factum.
Ego cogito ergo sum.
Errare humanum est, sed stultum est in errore perseverare.
Experientia est optima magistra.
Felix qui nihil debet.
Hic sunt dracones.
Hoc volo, sic jubeo, sit pro ratione voluntas.
Homo sum et nihil humani a me alienum puto.
Honores mutant mores, sed raro in meliores.
Ignorantia non est argumentum.
Multum, non multa.
Nihil habenti nihil deest.
Nemo omnia potest scire.
"""

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-c',
            '--count',
            type=int,
            default=5,
            help='Number of notes to add to each project',
        )

    def handle(self, *args, **options):
        if options['count']:
            Note.objects.bulk_create([
                Note(
                    project=project,
                    author=project.users.order_by('?').first(),
                    body=' '.join(choices(TEXT.split('\n'), k=randint(2, 4)))
                )
                for project in Project.objects.all()
                for _ in range(options['count'])
            ])
