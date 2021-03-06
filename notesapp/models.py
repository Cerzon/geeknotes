from django.db import models
from django.utils.translation import gettext_lazy as _

from usersapp.models import GeekUser


class Project(models.Model):
    name = models.CharField(_('name'), max_length=150)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    repo_url = models.URLField(_('link to repo'), max_length=250, blank=True)
    users = models.ManyToManyField(GeekUser, related_name='projects')

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.name}'


class Note(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(GeekUser, on_delete=models.PROTECT, related_name='notes')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    is_active = models.BooleanField(_('is active'), default=True)
    body = models.TextField(_('text'))

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'ToDo in {self.project} from {self.author}'
