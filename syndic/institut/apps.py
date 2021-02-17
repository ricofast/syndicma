from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InstitutConfig(AppConfig):
    name = "opencourse.institut"
    verbose_name = _("Instituts")

    def ready(self):
        import opencourse.institut.signals
