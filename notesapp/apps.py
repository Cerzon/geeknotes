from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotesappConfig(AppConfig):
    name = 'notesapp'
    verbose_name = _('notes')
