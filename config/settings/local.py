from .base import *  # noqa
from .base import env

DEBUG = True
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "yassaminefes.edussy.net", "yassaminecasa.edussy.net", "lavoisier.edussy.net", "public.edussy.net"]

INSTALLED_APPS += [
    # "debug_toolbar",
    "rosetta",
]
# MIDDLEWARE += [
#      "debug_toolbar.middleware.DebugToolbarMiddleware",
# ]
INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROSETTA_MESSAGES_PER_PAGE = 100
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
YANDEX_TRANSLATE_KEY = env.str("DJANGO_YANDEX_TRANSLATE_KEY", None)

ACCOUNT_EMAIL_VERIFICATION = "none"

ADMINS = (
    ("Admin", "admin@gmail.com"),
    ("Owner", "owner@gmail.com"),
)
