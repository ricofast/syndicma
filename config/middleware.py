import re

from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from opencourse.profiles.models import Student

#EXEMPT_URLS = [re.compile(reverse(settings.LOGIN_URL))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
    #print(EXEMPT_URLS)



class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        # print(request.path_info)
        # print(path)
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        # print(url_is_exempt)
        if path == reverse("account_logout").lstrip('/'):
            logout(request)
        if path == "admin/":
            return None

        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or url_is_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL)


class OneSessionPerUser:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.user.logged_in_user.session_key

            if current_session_key and current_session_key != request.session.session_key:
                Session.objects.get(session_key=current_session_key).delete()

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)
        return response






# class ParentKids:
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if request.user.is_parent:
#
#         if request.user.is_authenticated:
#             current_session_key = request.user.logged_in_user.session_key
#
#             if current_session_key and current_session_key != request.session.session_key:
#                 Session.objects.get(session_key=current_session_key).delete()
#
#             request.user.logged_in_user.session_key = request.session.session_key
#             request.user.logged_in_user.save()
#
#         response = self.get_response(request)
#         return response