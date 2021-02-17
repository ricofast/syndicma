from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig


class ClientsConfig(AppConfig):
    name = 'clients'
    verbose_name = _("Clients")

    # def ready(self):
    #     import opencourse.clients.handlers