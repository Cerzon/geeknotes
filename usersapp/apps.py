from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersappConfig(AppConfig):
    name = 'usersapp'
    verbose_name = _('users')
