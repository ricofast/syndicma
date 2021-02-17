from django.http import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy
from . import forms
from opencourse.profiles.models import LoggedInUser


class FormsetMixin(ModelFormMixin):
    formset_class = forms.SupplyFormset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = getattr(self, "object", None)
        if self.request.POST:
            context["formset"] = self.formset_class(
                self.request.POST, instance=instance
            )
        else:
            context["formset"] = self.formset_class(instance=instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class JsonFormMixin:
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse(form.data)

    def form_invalid(self, form):
        data = {
            "success": False,
            "errors": {k: v[0] for k, v in form.errors.items()},
        }
        return JsonResponse(data, status=400)


class ParentSelectedStudentMixin(PermissionRequiredMixin):
    kid = LoggedInUser.objects.all().first()

    login_url = reverse_lazy("profiles:403")

class AcademicYearMixin(object):
    #model = none
    def get_object(self):
        term = self.request.session.get('term')
        return term


class CoursePermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = "institut.manage_course"
    return_403 = True