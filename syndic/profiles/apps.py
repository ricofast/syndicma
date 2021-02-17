from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = "opencourse.profiles"
    verbose_name = _("Profiles")
