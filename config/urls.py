"""syndicma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog
from syndicma.profiles.views import ProfileView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # path("accounts/", include("allauth.urls")),
    # path("accounts/profile/", ProfileView.as_view()),
    path("profiles/", include("syndicma.profiles.urls", namespace="profiles")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("syndic/", include("syndicma.syndic.urls", namespace="syndic")),
    #path("schedule/", include("syndicma.schedule.urls", namespace="schedule")),
    path("", RedirectView.as_view(pattern_name="syndic:search")),
    #path("comments/", include('django_comments_xtd.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [path("rosetta/", include("rosetta.urls"))]
