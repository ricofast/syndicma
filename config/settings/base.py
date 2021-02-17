"""
Django settings for opencourse project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from email.utils import parseaddr

import environ
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
_ENV = env.str("DJANGO_SETTINGS_MODULE", "config.settings.base")
FIREBASE_CRED = env("FIREBASE_SCRED")
creed = os.path.join(BASE_DIR, FIREBASE_CRED)

# PROJECT_DIR = os.path.join(BASE_DIR, os.pardir)
#
# TENANT_APPS_DIR = os.path.join(PROJECT_DIR, os.pardir)
# sys.path.insert(0, TENANT_APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="!!!SET DJANGO_SECRET_KEY!!!",)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = []


# Application definition
SHARED_APPS = (

    "django_tenants",  # mandatory
    "clients.apps.ClientsConfig",  # you must list the app where your tenant model resides in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_crontab",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "modeltranslation",
    "crispy_forms",
    "django_filters",
    "guardian",
    "django_extensions",
    "embed_video",
    "import_export",
    "django_comments_xtd",
    "django_comments",
    "opencourse.profiles.apps.ProfilesConfig",

    "opencourse.institut.apps.InstitutConfig",
    "opencourse.quiz.apps.QuizConfig",
    "opencourse.essay.apps.EssayConfig",
    "opencourse.multichoice.apps.MCQConfig",
    "opencourse.true_false.apps.TruefalseConfig",
    "opencourse.schedule.apps.ScheduleConfig",
)


TENANT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_crontab",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "modeltranslation",
    "crispy_forms",
    "django_filters",
    "guardian",
    "django_extensions",
    "embed_video",
    "import_export",
    "django_comments_xtd",
    "django_comments",
    "opencourse.institut.apps.InstitutConfig",
    "opencourse.profiles.apps.ProfilesConfig",
    "opencourse.quiz.apps.QuizConfig",
    "opencourse.essay.apps.EssayConfig",
    "opencourse.multichoice.apps.MCQConfig",
    "opencourse.true_false.apps.TruefalseConfig",
    "opencourse.schedule.apps.ScheduleConfig",
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "clients.Client"  # app.Model

TENANT_DOMAIN_MODEL = "clients.Domain"  # app.Model

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)



ACCOUNT_DEFAULT_HTTP_PROTOCOL ="https"

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "config.middleware.LoginRequiredMiddleware",
    "config.middleware.OneSessionPerUser"
]

PUBLIC_SCHEMA_URLCONF = "config.public_urls"
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "opencourse/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "opencourse.institut.context_processors.academicyearname",
                "opencourse.institut.context_processors.academicyearnames",
                "opencourse.institut.context_processors.centername",
                "opencourse.institut.context_processors.cityname",
                "opencourse.institut.context_processors.notificates",
                "opencourse.institut.context_processors.schoolgroupname",
                "opencourse.institut.context_processors.loggedins",
                "opencourse.institut.context_processors.notifyStudent",
                "opencourse.institut.context_processors.activestudent",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'edussynetbase',
        'USER': 'postgres',
        'PASSWORD': 'Ayati2006!!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGES = (
#     ("fr", _("French")),
#     ("ar", _("العربية")),
#     ("en", _("English")),
# )
LANGUAGES = (
    ("fr", _("Français")),
    ("ar", _("العربية")),
    ("en", _("English")),
)


LANGUAGE_CODE = "fr"
MODELTRANSLATION_FALLBACK_LANGUAGES = ["fr", "ar", "en"]
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale/")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR("opencourse/static"))]
STATIC_ROOT = str(BASE_DIR("static"))

MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR("media"))

# Project adjustments
AUTH_USER_MODEL = "profiles.User"
admins_data = env.tuple(
    "DJANGO_ADMINS", default="Open Course <opencourse2020@mail.com>"
)
ADMINS = tuple(parseaddr(email) for email in admins_data)

# Third-party opencourse settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
)
SITE_ID = 1
CRISPY_TEMPLATE_PACK = "bootstrap4"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_FORMS = {"signup": "opencourse.profiles.forms.ProfileCreateForm"}
LOGIN_REDIRECT_URL = "profiles:dispatch_login"

ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"

LOGIN_URL = "account_login"
#LOGIN_URLS = '/accounts/login/'

LOGIN_EXEMPT_URLS = (
    r'^admin/$',
    r'^accounts/logout/$',
    r'^accounts/login/$',
    r'^accounts/signup/$',
    r'^accounts/password/change/$',
    r'^accounts/password/set/$',
    r'^accounts/password/reset/done/$',
    r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
    r'^accounts/password/reset/key/done/$',
    r'^accounts/password/reset/$',
)


GUARDIAN_RENDER_403 = True
GUARDIAN_TEMPLATE_403 = "403.html"
GUARDIAN_MONKEY_PATCH = False

# Security settings
CSRF_COOKIE_HTTPONLY = True
ADMIN_URL = "admin/"

# Delete on production
ACCOUNT_LOGOUT_ON_GET = True

CRONJOBS = [
    ('*/1 * * * *', 'opencourse.institut.cron.scheduled_job')
]

COMMENTS_APP = 'django_comments_xtd'

#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
                     b"Aequam memento rebus in arduis servare mentem.")
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_CONFIRM_EMAIL = True
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order')  # default is ('thread_id', 'order')

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = "opencourse2020@gmail.com"

# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = "opencourse2020@gmail.com"

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'institut.classe': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
    }
}
