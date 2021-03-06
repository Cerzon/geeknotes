from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class GeekUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        ordering = ('pk',)
