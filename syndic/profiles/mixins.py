from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from opencourse.profiles.models import User, Student

class ProfessorRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_professor_pages"
    login_url = reverse_lazy("profiles:403")


class StudentRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_student_pages"
    login_url = reverse_lazy("profiles:403")


class RegadminRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_regadmin_pages"
    login_url = reverse_lazy("profiles:403")


class SuperadminRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_superadmin_pages"
    login_url = reverse_lazy("profiles:403")


class ParentRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_parent_pages"
    login_url = reverse_lazy("profiles:403")


class AdminAllowedMixing(PermissionRequiredMixin):
    permission_required = ("","","","","")
    login_url = reverse_lazy("profiles:403")


class SuperadminAllowedMixing(PermissionRequiredMixin):
    permission_required = ("", "", "", "", "")
    login_url = reverse_lazy("profiles:403")


# class ParentKidsMixin(PermissionRequiredMixin):
#     if User.is_authenticated:
#         if User.is_parent:
#             kids = Student.objects.filter(parent=User.parents)
