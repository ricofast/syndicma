from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (
    UpdateView,
    RedirectView,
    CreateView,
    View,
    TemplateView,
    DetailView,
)
from tablib import Dataset
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from . import forms, models, admin
from .mixins import (
    ProfessorRequiredMixin,
    StudentRequiredMixin, RegadminRequiredMixin, SuperadminRequiredMixin, ParentRequiredMixin
)
from opencourse.institut.models import Course, Center

User = get_user_model()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name"]
    formset_class = None

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = self.formset_class(
                self.request.POST, self.request.FILES, instance=self.object
            )
            context["formset"] = self.formset_class(instance=self.object)
            # center = Center.objects.all().first()
            # context["center"] = center

        else:
            context["formset"] = self.formset_class(instance=self.object)
            # center = Center.objects.all().first()
            # context["center"] = center
        return context



    def form_valid(self, form):
        context = self.get_context_data(form=form)

        formset = context["formset"]
        # if formset.is_invalid():
        #     print("self.object111 =")
        #     print(self.object)
        #     return self.render_to_response(context)

        # print(formset)
        if formset.is_valid():
            # self.object = form.save()
            print("self.object =")
            print(self.object)
            # response = super().form_valid(form)

            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class ProfessorUpdateView(ProfessorRequiredMixin, ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("institut:list")
    formset_class = forms.ProfessorFormSet


class RegadminUpdateView(RegadminRequiredMixin, ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("institut:search")
    #formset_class = forms.RegadminFormSet


class ParentUpdateView(ParentRequiredMixin, ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("institut:search")
    #formset_class = forms.ParentFormSet


class SuperadminUpdateView(SuperadminRequiredMixin, ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("institut:search")
    #formset_class = forms.SuperadminFormSet


class StudentUpdateView(StudentRequiredMixin, ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("institut:search")
    formset_class = forms.StudentFormSet


class ProfileView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            return reverse_lazy("profiles:professor")
        elif hasattr(self.request.user, "student"):
            return reverse_lazy("profiles:student")
        elif hasattr(self.request.user, "parent"):
            return reverse_lazy("profiles:parent")
        elif hasattr(self.request.user, "regadmin"):
            return reverse_lazy("profiles:regadmin")
        elif hasattr(self.request.user, "superadmin"):
            return reverse_lazy("profiles:superadmin")
        return super().get_redirect_url(*args, **kwargs)


class DispatchLoginView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            if self.request.user.professor.course_set.exists():
                return reverse_lazy("institut:list")
            else:
                return reverse_lazy("institut:create")
        return reverse_lazy("institut:search")


class ReviewCreateView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    form_class = forms.ReviewForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("institut:detail", args=[pk])

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        pk = self.kwargs["pk"]
        course = Course.objects.filter(pk=pk).first()
        form.instance.professor = course.professor
        form.instance.coursename = course.title
        return super().form_valid(form)


class ContactRequestView(SingleObjectMixin, View):
    model = models.Professor

    def post(self, *args, **kwargs):
        professor = self.get_object()
        professor.contacts_requests += 1
        professor.save()
        return HttpResponse()


class StudentRequestView(DetailView, SingleObjectMixin):
    model = models.Student
    template_name = "profiles/student_detail.html"


class FreecoursesView(TemplateView):
    template_name = "../templates/freecourses.html"


class ForbiddenView(TemplateView):
    template_name = "../templates/403.html"


class ConditionsView(TemplateView):
    template_name = "../templates/conditions.html"


class PrivacyView(TemplateView):
    template_name = "../templates/privacy.html"


def user_upload(request):

    if request.method == 'POST':
        # student_resource = admin.StudentResource()
        file_format = request.POST['file-format']
        user_type = request.POST['user_type']
        dataset = Dataset()
        new_users = request.FILES['myfile']

        if file_format == 'XLSX':
            imported_data = dataset.load(new_users.read(), format='xlsx')
            # print(dataset[1])
            # result = student_resource.import_data(dataset, dry_run=True, raise_errors=True)
            # i = 0
            for data in imported_data:
                # print(dataset[i][1])
                # print(make_password(dataset[i][1]))
                # dataset[i][1] = make_password(dataset[i][1])
                # datax[i] = [None, data[0], data[1], None, 0, data[2], data[3], data[4], 0, 1, data[5]]
                value = models.User(
                    None,
                    make_password(data[1]),
                    None,
                    0,
                    data[0],
                    data[2],
                    data[3],
                    data[4],
                    0,
                    1,
                    data[5]
                )

                value.save()
                permission = get_object_or_404(
                    Permission, codename=f"access_{user_type}_pages"
                )

                value.user_permissions.add(permission)
                group_name = f"{user_type}s".capitalize()
                group, created = Group.objects.get_or_create(name=group_name)
                value.groups.add(group)
                user_type_class_map = {
                    "professor": models.Professor,
                    "student": models.Student,
                    "superadmin": models.Superadmin,
                    "regadmin": models.Regadmin,
                }
                user_class = user_type_class_map[user_type]
                profile = user_class()
                setattr(value, user_type, profile)
                profile.save()
                # i = i + 1
            # result = student_resource.import_data(dataset, dry_run=True, raise_errors=True)
        elif file_format == 'CSV':
            imported_data = dataset.load(new_users.read().decode('utf-8'), format='csv')
            # result = student_resource.import_data(dataset, dry_run=True, raise_errors=True)
            # i = 0
            for data in imported_data:
                # dataset[i][1] = make_password(dataset[i][1])
                # print(data[1])
                value = models.User(
                    None,
                    make_password(data[1]),
                    None,
                    0,
                    data[0],
                    data[2],
                    data[3],
                    data[4],
                    0,
                    1,
                    data[5]
                )
                value.save()
                permission = get_object_or_404(
                    Permission, codename=f"access_{user_type}_pages"
                )

                value.user_permissions.add(permission)
                group_name = f"{user_type}s".capitalize()
                group, created = Group.objects.get_or_create(name=group_name)
                value.groups.add(group)
                # i = i + 1
            # result = student_resource.import_data(dataset, dry_run=True, raise_errors=True)
        elif file_format == 'XLS':
            imported_data = dataset.load(new_users.read(), format='xls')
            # result = student_resource.import_data(dataset, dry_run=True, raise_errors=True)
            # i = 0
            for data in imported_data:
                # dataset[i][1] = make_password(dataset[i][1])
                # print(data[1])
                value = models.User(
                    None,
                    make_password(data[1]),
                    None,
                    0,
                    data[0],
                    data[2],
                    data[3],
                    data[4],
                    0,
                    1,
                    data[5]
                )
                value.save()
                permission = get_object_or_404(
                    Permission, codename=f"access_{user_type}_pages"
                )

                value.user_permissions.add(permission)
                group_name = f"{user_type}s".capitalize()
                group, created = Group.objects.get_or_create(name=group_name)
                value.groups.add(group)
                # i = i + 1
            # result = student_resource.import_data(dataset, dry_run=True, raise_errors=True)
        # print(imported_data)

        # if result.has_errors():
        #     messages.error(request, 'Uh oh! Something went wrong...')
        # #
        # #     # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import
        # #
        # else:
        #     student_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'profiles/upload_users.html')
