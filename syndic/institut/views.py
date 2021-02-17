from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.formats import date_format
from datetime import date
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    FormView,
    UpdateView,
    DetailView,
    DeleteView,
    TemplateView,
    View,
)
from django.contrib.auth.decorators import login_required

from django_filters.views import FilterView

from guardian.shortcuts import assign_perm

from . import forms, models, filters
from opencourse.profiles.models import Student, Professor, Review, Superadmin, Regadmin
from .mixins import FormsetMixin, JsonFormMixin, AcademicYearMixin, CoursePermissionRequiredMixin
from opencourse.profiles.forms import ReviewForm
from opencourse.profiles.mixins import ProfessorRequiredMixin, StudentRequiredMixin, SuperadminRequiredMixin, RegadminRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from django.db.models import Q
from urllib.parse import urlparse

REVIEW_COUNT = 10

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


class AcademicyearEditView(LoginRequiredMixin, UpdateView):
    permission_required = "institut.manage_academicyear"
    model = models.Academicyear
    form_class = forms.AcademicYearForm
    template_name = "institut/acayear_edit.html"


class HolidaysSearchResultsView(LoginRequiredMixin, FilterView):
    filterset_class = filters.HolidaysFilter
    template_name = "institut/holidays_search_results.html"


class HolidaysCreateView(LoginRequiredMixin, CreateView):
    permission_required = "institut.manage_holidays"
    model = models.Holidays
    form_class = forms.HolidaysForm
    template_name = "institut/holidays_edit.html"
    success_url = reverse_lazy("institut:holidays_list")


class HolidaysEditView(LoginRequiredMixin, UpdateView):
    permission_required = "institut.manage_holidays"
    model = models.Holidays
    form_class = forms.HolidaysForm
    template_name = "institut/holidays_edit.html"
    success_url = reverse_lazy("institut:holidays_list")


class HolidaysListView(LoginRequiredMixin, ListView):
    permission_required = "institut.manage_holidays"
    model = models.Holidays
    template_name = "institut/holidays_list.html"


class HolidaysDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.manage_holidays"
    model = models.Holidays
    success_url = reverse_lazy("institut:holidays_delete")
    template_name = "confirm_delete.html"


class SchoolgroupCreateView(LoginRequiredMixin, CreateView):
    permission_required = "institut.manage_schoolgroup"
    model = models.Schoolgroup
    template_name = "institut/schoolgroup_edit.html"
    form_class = forms.SchoolgroupForm
    success_url = reverse_lazy("institut:schoolgroups:list")

    def form_valid(self, form):
        form.instance.admin = self.request.user.superadmin
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs["title"] = _("Create Your School Group")
        return super(SchoolgroupCreateView, self).get_context_data(**kwargs)


class SchoolgroupEditView(LoginRequiredMixin, UpdateView):
    permission_required = "institut.manage_schoolgroup"
    model = models.Schoolgroup
    template_name = "institut/schoolgroup_edit.html"
    form_class = forms.SchoolgroupForm
    success_url = reverse_lazy("institut:schoolgroups:list")

    def form_valid(self, form):
        form.instance.admin = self.request.user.superadmin
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs["title"] = _("Update Your School Group")
        return super(SchoolgroupEditView, self).get_context_data(**kwargs)


class SchoolgroupListView(LoginRequiredMixin, ListView):
    permission_required = "institut.manage_schoolgroup"
    model = models.Schoolgroup
    template_name = "institut/schoolgroup_list.html"


class SchoolgroupdeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.manage_schoolgroup"
    model = models.Schoolgroup
    success_url = reverse_lazy("institut:schoolgroups:list")
    template_name = "confirm_delete.html"


class CenterCreateView(LoginRequiredMixin, CreateView):
    permission_required = "institut.add_center"
    model = models.Center
    template_name = "institut/center_edit.html"
    form_class = forms.CenterForm
    success_url = reverse_lazy("institut:centers:list")

    def form_valid(self, form):
        form.instance.admin = self.request.user.superadmin
        form.save()
        return super().form_valid(form)


class CenterEditView(LoginRequiredMixin, UpdateView):
    permission_required = "institut.manage_center"
    model = models.Center
    template_name = "institut/center_edit.html"
    form_class = forms.CenterForm
    success_url = reverse_lazy("institut:centers:list")

    def form_valid(self, form):
        form.instance.admin = self.request.user.superadmin
        form.save()
        return super().form_valid(form)


class CenterListView(SuperadminRequiredMixin, ListView):
    permission_required = "institut.manage_center"
    model = models.Center
    template_name = "institut/centers_list.html"


class CenterDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.delete_center"
    model = models.Center
    success_url = reverse_lazy("institut:centers:list")
    template_name = "confirm_delete.html"


class CenterlevelListView(LoginRequiredMixin, ListView):
    permission_required = "institut.manage_centerlevel"
    model = models.Centerlevel
    template_name = "institut/centerlvls_list.html"


class CenterlevelEditView(LoginRequiredMixin, UpdateView):
    permission_required = "institut.manage_centerlevel"
    model = models.Centerlevel
    template_name = "institut/centerlvls_edit.html"
    form_class = forms.CenterlevelForm
    success_url = reverse_lazy("institut:centers:centerlvl_list")


class CenterlevelCreateView(LoginRequiredMixin, CreateView):
    permission_required = "institut.add_centerlevel"
    model = models.Centerlevel
    template_name = "institut/centerlvls_edit.html"
    form_class = forms.CenterlevelForm
    success_url = reverse_lazy("institut:centers:centerlvl_list")


class CenterlevelDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.delete_centerlevel"
    model = models.Centerlevel
    success_url = reverse_lazy("institut:centers:centerlvl_list")
    template_name = "confirm_delete.html"


class GradeListView(LoginRequiredMixin, ListView):
    permission_required = "institut.manage_grade"
    model = models.Grade
    template_name = "institut/grade_list.html"
    paginate_by = 100  # if pagination is desired


class GradeCreateView(LoginRequiredMixin, FormsetMixin, CreateView):
    permission_required = "institut.add_grade"
    model = models.Grade
    form_class = forms.GradeForm
    formset_class = forms.ClasseFormset
    template_name = "institut/grade_edit.html"

    success_url = reverse_lazy("institut:gradelist")


class GradeEditeView(LoginRequiredMixin, FormsetMixin, UpdateView):
    permission_required = "institut.manage_grade"
    model = models.Grade
    form_class = forms.GradeForm
    formset_class = forms.ClasseFormset
    template_name = "institut/grade_edit.html"

    success_url = reverse_lazy("institut:gradelist")


class GradeDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.delete_grade"
    model = models.Grade
    success_url = reverse_lazy("institut:gradelist")
    template_name = "confirm_delete.html"


class ClasseProfView(LoginRequiredMixin, DetailView):
    permission_required = "institut.manage_classe"
    model = models.Classe
    template_name = "institut/classe_prof.html"

    def get_context_data(self, **kwargs):
        professor = self.request.user.professor
        kwargs["mycourses"] = models.Course.objects.filter(classe=self.object, professor=professor)
        kwargs["courses"] = models.Course.objects.filter(classe=self.object).exclude(professor=professor)
        kwargs["students"] = self.object.student.order_by("id")
        kwargs["student_count"] = self.object.student.count()
        return super().get_context_data(**kwargs)


class ClasseListView(LoginRequiredMixin, AcademicYearMixin, ListView):
    permission_required = "institut.manage_classe"
    model = models.Classe
    template_name = "institut/classe_list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        aca_year = self.get_object()
        classes = models.Classe.objects.filter(academicyear=aca_year).order_by("grade")
        return classes


class ClasseProfListView(ProfessorRequiredMixin, AcademicYearMixin, ListView):
    model = models.Classe
    template_name = "institut/classe_list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        professor = self.request.user.professor
        aca_year = self.get_object()
        classes = models.Classe.objects.filter(course__professor=professor, academicyear=aca_year).distinct()
        return classes


class ClasseCreateView(LoginRequiredMixin, AcademicYearMixin, CreateView):
    permission_required = "institut.manage_classe"
    model = models.Classe
    form_class = forms.ClasseForm
    template_name = "institut/classe_create.html"
    exclude = ["academicyear"]
    success_url = reverse_lazy("institut:classlist")
    def form_valid(self, form):
        aca_year = self.get_object()
        form.instance.academicyear = models.Academicyear.objects.get(pk=aca_year)
        form.save()
        return super().form_valid(form)


class ClasseEditeView(LoginRequiredMixin, UpdateView):
    permission_required = "institut.manage_classe"
    model = models.Classe
    form_class = forms.ClasseEditForm
    template_name = "institut/classe_edit.html"
    success_url = reverse_lazy("institut:classlist")

    def get_context_data(self, **kwargs):
        kwargs["courses"] = self.object.course_set.order_by("-id")
        kwargs["students"] = self.object.student.order_by("-id")[:6]
        kwargs["student_count"] = self.object.student.count()
        return super().get_context_data(**kwargs)


class ClasseDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.manage_classe"
    model = models.Classe
    success_url = reverse_lazy("institut:classlist")
    template_name = "confirm_delete.html"


class CourseEditView(LoginRequiredMixin, FormsetMixin, UpdateView):
    permission_required = "institut.manage_course"
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.SupplyFormset
    template_name = "institut/course_edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("institut:list")

    return_403 = True

    def get_form_kwargs(self):
        kwargs = super(CourseEditView, self).get_form_kwargs()
        kwargs.update({"professor": self.request.user.professor})
        return kwargs


class CourseEdittimeView(RegadminRequiredMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    template_name = "institut/course_manage.html"
    #permission_required = "institut.manage_course"

    def get_success_url(self):
        course_pk = self.kwargs.get("pk")
        classe = get_object_or_404(models.Classe, course=course_pk)
        return reverse("institut:classedit", kwargs={"pk": classe.pk})


class CourseCreateView(LoginRequiredMixin, CreateView):
    permission_required = "institut.manage_course"
    model = models.Course
    form_class = forms.CourseForm
    template_name = "institut/course_manage.html"

    def get_success_url(self):
        classe_pk = self.kwargs.get("classe_pk")
        return reverse("institut:classedit", kwargs={"pk": classe_pk})

    def get_initial(self):
        initial = {
            "area": 1,
            "language": 1,

        }
        return initial

    def form_valid(self, form):
        with transaction.atomic():
            professor = form.instance.professor
            form.instance.created_by = self.request.user
            response = super().form_valid(form)
            assign_perm("manage_course", professor.user, self.object)
            return response

    def get_context_data(self, **kwargs):
        classe_pk = self.kwargs.get("classe_pk")
        kwargs["classe"] = models.Classe.objects.get(pk=classe_pk)
        return super().get_context_data(**kwargs)


class CourseListView(LoginRequiredMixin, AcademicYearMixin, ListView):
    permission_required = "institut.manage_course"
    template_name = "institut/course_list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        professor = self.request.user.professor
        aca_year = self.get_object()
        return models.Course.objects.created_by(professor=professor, aca_year=aca_year)


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.manage_course"
    model = models.Course
    success_url = reverse_lazy("institut:list")
    template_name = "confirm_delete.html"


class CourseStudentsListView(ProfessorRequiredMixin, ListView):
    model = models.Course
    template_name = "institut/course_students_list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        course = get_object_or_404(models.Course, pk=self.kwargs.get("pk"))
        students = Student.objects.filter(
            enrollment__course=course, enrollment__accepted=True
        )
        return students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(models.Course, pk=self.kwargs.get("pk"))
        return context


class HowToView(TemplateView):
    template_name = "base3.html"

class FirebaseView(TemplateView):
    template_name = "institut/firebase.html"
    # def get_context_data(self, **kwargs):
    #     center = models.Center.objects.all().first()
    #     kwargs["center"] = center
    #     return super(HowToView, self).get_context_data(**kwargs)


class CalenderEditView(LoginRequiredMixin, ListView):
    permission_required = "institut.change_coursetime"
    model = models.Coursetime
    template_name = "institut/calender.html"

    def get_queryset(self):
        classe_pk = self.kwargs.get("pk")
        classe = get_object_or_404(models.Classe, pk=classe_pk)
        object_list = self.model.objects.filter(
            course__classe=classe
        ).order_by("id")
       # object_list = self.model.objects.course.coursetime_set.order_by("id")
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classe_pk = self.kwargs.get("pk")
        context["courses"] = models.Course.objects.filter(classe=classe_pk).order_by("id")
        context["classe"] = models.Classe.objects.get(pk=classe_pk)
        return context


class ProfCalenderView(ProfessorRequiredMixin, ListView):
    model = models.Coursetime
    template_name = "institut/profcalender.html"

    def get_queryset(self):
        prof_pk = self.kwargs.get("prof_pk")
        professor = get_object_or_404(Professor, pk=prof_pk)
        object_list = models.Coursetime.objects.filter(course__professor=professor)
        return object_list

    def get_context_data(self, **kwargs):
        prof_pk = self.kwargs.get("prof_pk")
        kwargs["user_cal"] = get_object_or_404(Professor, pk=prof_pk)

        return super(ProfCalenderView, self).get_context_data(**kwargs)


class StudentCalenderView(LoginRequiredMixin, ListView):
    model = models.Coursetime
    template_name = "institut/profcalender.html"

    def get_queryset(self):
        student_pk = self.kwargs.get("student_pk")
        student = get_object_or_404(Student, pk=student_pk)

        kids = Student.objects.filter(parent=self.request.user.parent)
        if student_pk in [i.pk for i in kids]:
            object_list = models.Coursetime.objects.filter(course__classe__student=student)
            return object_list
        else:
            object_list = {}
            return object_list

    def get_context_data(self, **kwargs):
        student_pk = self.kwargs.get("student_pk")
        kids = Student.objects.filter(parent=self.request.user.parent)
        if student_pk in [i.pk for i in kids]:
            kwargs["user_cal"] = get_object_or_404(Student, pk=student_pk)
        else:
            kwargs["user_cal"] = ""

        return super(StudentCalenderView, self).get_context_data(**kwargs)


class AgendaCalenderView(LoginRequiredMixin, ListView):
    model = models.CourseOutline
    template_name = "institut/agendacalender.html"

    def get_queryset(self):
        classe_pk = self.kwargs.get("classe_pk")
        classe = get_object_or_404(models.Classe, pk=classe_pk)
        dt = date_format(date.today(), 'W')

        outline_list = self.model.objects.filter(course__classe=classe, weekdue=dt).values("id", "course", "name",
                                                                                                    "datedue")

        work_list = models.CourseWork.objects.filter(course__classe=classe, weekdue=dt).values("id", "course", "name",
                                                                                               "datedue")
        object_list = list(chain(outline_list, work_list))

        return object_list

    def get_context_data(self, **kwargs):
        classe_pk = self.kwargs.get("classe_pk")
        kwargs["classe"] = get_object_or_404(models.Classe, pk=classe_pk)

        return super(AgendaCalenderView, self).get_context_data(**kwargs)


class ClasseCalenderView(LoginRequiredMixin, ListView):
    model = models.Coursetime
    template_name = "institut/classecalender.html"

    def get_queryset(self):
        classe_pk = self.kwargs.get("classe_pk")
        classe = get_object_or_404(models.Classe, pk=classe_pk)
        object_list = models.Coursetime.objects.filter(course__classe=classe)
        return object_list

    def get_context_data(self, **kwargs):
        classe_pk = self.kwargs.get("classe_pk")
        kwargs["classe"] = get_object_or_404(models.Classe, pk=classe_pk)
        return super(ClasseCalenderView, self).get_context_data(**kwargs)


@login_required
def calendar(request):
    all_events = models.Events.objects.all()
    all_courses = models.Course.objects.all()
    context = {
        "events": all_events,
        "courses": all_courses,
    }
    return render(request, 'institut/calendar.html', context)


@login_required
def add_event(request):
    courseid = request.GET.get("courseid", None)
    course = models.Course.objects.get(id=courseid)
    #print(course)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = course.title
    event = models.Coursetime(course=course, name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)


@login_required
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = models.Coursetime.objects.get(id=id)
    course = event.course
    event.start = start
    event.end = end
    event.name = title

    event.save()
    data = {}
    return JsonResponse(data)


@login_required
def remove(request):
    id = request.GET.get("id", None)
    event = models.Coursetime.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)


class AddeventView(LoginRequiredMixin, JsonFormMixin, CreateView):
    permission_required = "institut.manage_coursetime"
    model = models.Coursetime

    def get(self, request, *args, **kwargs):
        postdata = request.GET
        courseid = postdata.get("courseid", None)
        course = get_object_or_404(models.Course, pk=courseid)
        type = postdata.get("type", None)
        start = postdata.get("start", None)
        starttime = postdata.get("starttime", None)
        endtime = postdata.get("endtime", None)
        #print(starttime)
        end = postdata.get("end", None)
        title = course.title + '-' + course.classe.name
        courseday = postdata.get("courseday", None)
        event = models.Coursetime(course=course, name=str(title), start=start, end=end, type=type,
                                  courseday=str(courseday), starttime=starttime, endtime=endtime)
        event.save()
        data = {}
        return JsonResponse(data)


class UpdateeventView(LoginRequiredMixin, JsonFormMixin, UpdateView):
    permission_required = "institut.manage_coursetime"
    model = models.Coursetime

    def get(self, request, *args, **kwargs):
        postdata = request.GET
        courseid = postdata.get("courseid", None)

        start = postdata.get("start", None)
        end = postdata.get("end", None)
        starttime = postdata.get("starttime", None)
        endtime = postdata.get("endtime", None)
        title = postdata.get("title", None)
        courseday = postdata.get("courseday", None)
        id = postdata.get("id", None)
        type = postdata.get("type", None)
        event = models.Coursetime.objects.get(id=id)
        event.start = start
        event.end = end
        event.starttime = starttime
        event.endtime = endtime
        event.courseday = str(courseday)

        if courseid:
            course = get_object_or_404(models.Course, pk=courseid)
            event.course = course

            event.name = str(course.title + '-' + course.classe.name)
            event.type = type
        else:
            event.name = title


        event.save()
        data = {}
        return JsonResponse(data)

class AttendanceListView(LoginRequiredMixin, ListView):
    permission_required = "institut.manage_attendance"
    model = models.Attendance
    template_name = "institut/attendance_list.html"

    def get_queryset(self):
        student_pk = self.kwargs.get("student_pk")
        student = get_object_or_404(Student, pk=student_pk)

        kids = Student.objects.filter(parent=self.request.user.parent)
        if student_pk in [i.pk for i in kids]:
            object_list = self.model.objects.filter(student=student)
            return object_list
        else:
            object_list = {}
            return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_pk = self.kwargs.get("student_pk")
        context["student"] = get_object_or_404(Student, pk=student_pk)
        # context["courses"] = models.Course.objects.filter(classe=classe_pk).order_by("id")
        # context["classe"] = models.Classe.objects.get(pk=classe_pk)
        return context


class AttendanceView(LoginRequiredMixin, ListView):
    model = models.Attendance
    template_name = "institut/attendance.html"

    def get_context_data(self, **kwargs):
        coursetime_pk = self.kwargs.get("coursetime_pk")
        attendancedate= self.kwargs.get("at_date")

        coursetime = get_object_or_404(models.Coursetime, pk=coursetime_pk)
        attendancelist = self.model.objects.filter(coursetime=coursetime, attendancedate=attendancedate)

        kwargs["attendance_list"] = attendancelist
        course = models.Course.objects.filter(coursetime=coursetime).first()
        kwargs["coursetimes"] = models.Coursetime.objects.filter(course=course)
        kwargs["ncoursetimes"] = models.Coursetime.objects.filter(course=course).count()
        classe = models.Classe.objects.filter(course=course).first()
        kwargs["coursetime"] = coursetime
        kwargs["course"] = course
        kwargs["classe"] = classe
        kwargs["students"] = Student.objects.filter(classe=classe)
        kwargs["student_count"] = Student.objects.filter(classe=classe).count()
        return super(AttendanceView, self).get_context_data(**kwargs)


class AttendanceCreateView(LoginRequiredMixin, JsonFormMixin, CreateView):
    permission_required = "institut.manage_attendance"
    model = models.Attendance

    def get(self, request, *args, **kwargs):
        postdata = request.GET
        coursetimeid = postdata.get("coursetimeid", None)
        coursetime = get_object_or_404(models.Coursetime, pk=coursetimeid)
        studentid = postdata.get("studentid", None)
        student = get_object_or_404(Student, pk=studentid)
        status = postdata.get("status", None)
        attendancedate = postdata.get("attendancedate", None)
        event = models.Attendance(coursetime=coursetime, student=student, attendancedate=attendancedate, status=status)
        event.save()
        data = {}
        return JsonResponse(data)


class ProfessorDashboardView(ProfessorRequiredMixin, AcademicYearMixin, TemplateView):
    template_name = "institut/prof_dashboard.html"

    def get_context_data(self, **kwargs):
        professor = self.request.user.professor
        acay = self.get_object()
        kwargs["courses"] = models.Course.objects.filter(professor=professor, classe__academicyear=acay)
        kwargs["coursetimes"] = models.Coursetime.objects.filter(course__professor=professor,
                                                                 course__classe__academicyear=acay)
        dt = date_format(date.today(), 'w')
        kwargs["classes"] = models.Classe.objects.filter(course__professor=professor, academicyear=acay).distinct()
        kwargs["currenttimes"] = models.Coursetime.objects.filter(course__professor=professor,
                                                                  courseday__exact=dt,
                                                                  course__classe__academicyear=acay).order_by(
            "starttime")
        return super(ProfessorDashboardView, self).get_context_data(**kwargs)


class StudentDashboardView(LoginRequiredMixin, AcademicYearMixin, TemplateView):
    template_name = "institut/student_dashboard.html"

    def get_context_data(self, **kwargs):
        kid = self.request.session.get('kid')
        if not kid:
            if hasattr(self.request.user, "parent"):
                kids = Student.objects.filter(parent=self.request.user.parent).first()
                kid = kids.pk
                self.request.session['kid'] = kid
                student = get_object_or_404(Student, pk=kid)
            elif hasattr(self.request.user, "student"):
                student = self.request.user.student
        else:
            student = get_object_or_404(Student, pk=kid)


        acay = self.get_object()

        kwargs["courses"] = models.Course.objects.filter(classe__student=student, classe__academicyear=acay)
        kwargs["coursetimes"] = models.Coursetime.objects.filter(course__classe__student=student,
                                                                 course__classe__academicyear=acay)
        dt = date_format(date.today(), 'w')
        kwargs["classe"] = models.Classe.objects.filter(student=student, academicyear=acay).first()
        kwargs["currenttimes"] = models.Coursetime.objects.filter(course__classe__student=student,
                                                                  courseday__exact=dt,
                                                                  course__classe__academicyear=acay).order_by(
            "starttime")
        return super(StudentDashboardView, self).get_context_data(**kwargs)


class CourseOutlineListView(LoginRequiredMixin, ListView):
    model = models.CourseOutline
    template_name = "institut/courseoutline_list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        course_pk = self.kwargs.get("course_pk")
        course = get_object_or_404(models.Course, pk=course_pk)
        object_list = self.model.objects.filter(
            course=course
        ).order_by("-id")
        return object_list

    def get_context_data(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        kwargs["course"] = get_object_or_404(models.Course, pk=course_pk)
        return super(CourseOutlineListView, self).get_context_data(**kwargs)


class CourseOutlineCreateView(LoginRequiredMixin, CreateView):
    permission_required = "institut.manage_courseoutline"
    model = models.CourseOutline
    form_class = forms.CourseOutlineForm
    template_name = "institut/courseoutline_edit.html"
    exclude = ["course"]
    def get_success_url(self):
        course_pk = self.kwargs.get("course_pk")
        return reverse("institut:courseoutline_list", kwargs={"course_pk": course_pk})

    def form_valid(self, form):
        with transaction.atomic():
            course_pk = self.kwargs.get("course_pk")
            course = get_object_or_404(models.Course, pk=course_pk)
            coursetimes = models.Coursetime.objects.filter(course=course)
            form.instance.course = course

            if int(date_format(form.cleaned_data['datedue'], 'w')) not in [i.courseday for i in coursetimes]:
                form.add_error('datedue', 'the date you choose doesnt correspond to a valid course time')
                return self.form_invalid(form)

            response = super().form_valid(form)
            #course = self.object
            # print(course)
            # print(self.request.user.professor)
            assign_perm("manage_courseoutline", course.professor.user, self.object)
            return response

    # def get_form_kwargs(self):
    #     kwargs = super(CourseOutlineCreateView, self).get_form_kwargs()
    #     print(kwargs)
    #     course_pk = self.kwargs.get("course_pk")
    #     print(course_pk)
    #     course = get_object_or_404(models.Course, pk=course_pk)
    #     print(course)
    #     kwargs.update({"course": course})
    #     return kwargs


class CourseOutlineEditView(LoginRequiredMixin, UpdateView):
    permission_required = "institut.manage_courseoutline"
    model = models.CourseOutline
    form_class = forms.CourseOutlineForm
    template_name = "institut/courseoutline_edit.html"
    success_url = reverse_lazy("institut:courseoutline_list")

    def get_success_url(self):
        courseoutline= self.kwargs.get("pk")
        course = models.Course.objects.get(courseoutline=courseoutline)
        return reverse("institut:courseoutline_list", kwargs={"course_pk": course.pk})


class CourseOutlineDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = "institut.manage_courseoutline"
    model = models.CourseOutline
    success_url = reverse_lazy("institut:courseoutline_list")
    template_name = "confirm_delete.html"


class ParentNotifyListView(LoginRequiredMixin, ListView):
    model = models.ParentNotification
    template_name = "institut/parentnotify_list.html"
    #paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        kid = self.request.session.get('kid')
        term = self.request.session.get('term')
        #print(kid)
        if not term:
            acayears = models.Academicyear.objects.last()
            self.request.session['term'] = acayears.pk
        else:
            acayear = models.Academicyear.objects.get(pk=term)


        if not kid:
            kids = Student.objects.filter(parent=self.request.user.parent).first()
            kid = kids.pk
        self.request.session['kid'] = kid

        #student_pk = self.kwargs.get("student_pk")
        student = get_object_or_404(Student, pk=kid)
        #print(student)
        object_list = self.model.objects.filter(student__parent=self.request.user.parent, student=student,
                                                course__classe__academicyear=acayear)
        # print(kids)
        # print('kid is')
        # print(kid)
        # if kid in [i.pk for i in kids]:
        #     object_list = self.model.objects.filter(
        #         student=student
        #     ).order_by("-notifydate")
        #     print(object_list)
        #     return object_list
        # else:
        #     object_list = {}
        #     return object_list
        return object_list


class ParentNotifyUpdateView(LoginRequiredMixin, JsonFormMixin, UpdateView):
    model = models.ParentNotification

    def get(self, request, *args, **kwargs):
        postdata = request.GET
        notifyid = postdata.get("notifyid", None)
        notify = get_object_or_404(self.model, pk=notifyid)
        notify.parentread = True
        notify.save()

        data = {}
        return JsonResponse(data)


@login_required
def parentkidselect(request):
    kid = request.GET.get("kid", None)
    request.session['kid'] = kid
    data = {}
    return JsonResponse(data)


@login_required
def acayearselect(request):
    ayear = request.GET.get("ayear", None)
    request.session['term'] = ayear
    data = {}
    return JsonResponse(data)


class MessageSendView(LoginRequiredMixin, AcademicYearMixin, TemplateView):
    #permission_required = "institut.manage_attendance"
    # model = models.Notification
    # form_class = forms.NotificationForm
    template_name = "institut/message_edit.html"

    def get_context_data(self, **kwargs):
        acay = self.get_object()
        if self.request.user.is_professor:
            professor = self.request.user.professor
            classes = models.Classe.objects.filter(course__professor=professor, academicyear=acay).distinct()
        elif self.request.user.is_regadmin or self.request.user.is_superadmin:
            classes = models.Classe.objects.filter(academicyear=acay).distinct()
        kwargs["classes"] = classes

        kwargs["messages"] = models.NotificationLog.objects.filter(admin=self.request.user).order_by('-id')[:6]
        kwargs["messages_count"] = models.NotificationLog.objects.filter(admin=self.request.user).count()
        return super().get_context_data(**kwargs)


class SaveMessageView(LoginRequiredMixin, JsonFormMixin, CreateView):
    model = models.Notification

    def get(self, request, *args, **kwargs):
        postdata = request.GET
        subject = postdata.get("subject")
        text = postdata.get("text")
        classid = postdata.get("classid")
        students = postdata.getlist("studentid[]")

        for studentid in students:
            if studentid == 'all':
                classe = get_object_or_404(models.Classe, pk=classid)
                studentlist = Student.objects.filter(classe=classe)
                for studentc in studentlist:
                    notify = models.Notification(admin=self.request.user, student=studentc, subject=subject, text=text,
                                                 parentread=False, studentread=False)
                    notify.save()
                notifylog = models.NotificationLog(admin=self.request.user, receiver=classe.name, subject=subject,
                                                   text=text)
                notifylog.save()

            else:
                student = get_object_or_404(Student, pk=studentid)
                notify = models.Notification(admin=self.request.user, student=student, subject=subject, text=text,
                                         parentread=False, studentread=False)
                notify.save()
                studentname = student.user.first_name + ' ' + student.user.last_name
                notifylog = models.NotificationLog(admin=self.request.user, receiver=studentname, subject=subject,
                                                   text=text)
                notifylog.save()
        data = {}
        return JsonResponse(data)


@login_required
def deletemessage(request):
    id = request.GET.get("messageid", None)
    event = models.NotificationLog.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)


class MessagesListView(LoginRequiredMixin, ListView):
    model = models.NotificationLog
    template_name = "institut/messages_list.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(
            admin=self.request.user
        )
        return object_list

class MsgSendView(LoginRequiredMixin, AcademicYearMixin, CreateView):
    model = models.Notification
    form_class = forms.NotificationForm
    template_name = "institut/message_edit.html"
    success_url = reverse_lazy("institut:message")

    def form_valid(self, form):
        form.instance.admin = self.request.user
        students = self.request.POST.getlist("student")
        #students = self.request.POST.get("student")
        print("students:")
        print(students)

        if not students:
            form.add_error('You must choose a student')
            return self.form_invalid(form)

        for student in students:
            form.instance.student = get_object_or_404(Student, pk=student)
            form.save()
        #form.instance.student.set(students)

        # form.instance.type = "M"
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MessageSendView, self).get_form_kwargs()
        kwargs.update({"admin": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        acay = self.get_object()

        if self.request.user.is_professor:
            professor = self.request.user.professor
            classes = models.Classe.objects.filter(course__professor=professor, academicyear=acay).distinct()
            # for classe in classes:
            #     students = students | Student.objects.filter(classe=classe)
        elif self.request.user.is_regadmin or self.request.user.is_superadmin:
            classes = models.Classe.objects.filter(academicyear=acay).distinct()
            # for classe in classes:
            #     students = students | Student.objects.filter(classe=classe)
        # print(students)
        kwargs["classes"] = classes
        #kwargs["students"] = students
        return super().get_context_data(**kwargs)


def load_students(request):
    classe_id = request.GET.get('classe')
    if classe_id:
        classe = get_object_or_404(models.Classe, pk=classe_id)
    # classe = models.Classe.objects.filter(course=course).first()
    # print(classe)

        students = Student.objects.filter(classe=classe)
        # studentlist =[]
        # for student in students:
        #     studentlist.append([student.id,student.user.first_name, student.user.last_name, student.user.email, student.parent.user.email, "select"])
        #studentlist=list(students)
        #print(studentlist)
        return render(request, 'institut/student_dropdown_list.html', {'students': students})
    else:
        return render(request, 'institut/student_dropdown_list.html')




# ********************************************************************************
# ***************** OLD Views ****************************************************
# ********************************************************************************

class CenterDetailView(DetailView, MultipleObjectMixin):
    model = models.Center
    template_name = "institut/center_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        professor = getattr(self.request.user, "professor", None)
        kwargs["join_request_form"] = forms.JoinRequestCreateForm(
            initial={"center": self.object, "professor": professor},
        )
        join_request = models.JoinRequest.objects.filter(
            center=self.object, professor=professor
        ).first()
        kwargs["join_request_accepted"] = getattr(
            join_request, "accepted", "not_existing"
        )
        object_list1 = models.JoinRequest.objects.filter(
            center=self.object
        )
        object_list = models.Course.objects.filter(center=self.get_object())
        return super(CenterDetailView, self).get_context_data(
            object_list=object_list, object_list1=object_list1, **kwargs
        )


class CenterSearchResultsView(FilterView):
    filterset_class = filters.CenterFilter
    template_name = "institut/center_search_results.html"
    paginate_by = 10


class JoinRequestCreateView(ProfessorRequiredMixin, JsonFormMixin, CreateView):
    model = models.JoinRequest
    form_class = forms.JoinRequestCreateForm


class JoinRequestUpdateView(ProfessorRequiredMixin, JsonFormMixin, UpdateView):
    model = models.JoinRequest
    fields = ["accepted"]


class JoinRequestrListView(ProfessorRequiredMixin, ListView):
    model = models.JoinRequest
    template_name = "institut/join_request_list.html"
    paginate_by = 15

    def get_queryset(self):
        object_list = self.model.objects.filter(
            center__admin=self.request.user.professor
        ).order_by("accepted")
        return object_list


class CourseDetailView(DetailView):
    model = models.Course
    template_name = "institut/course_details.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs["review_form"] = ReviewForm()
        kwargs["professor"] = self.object.professor
        kwargs["reviews"] = self.object.professor.review_set.order_by("-id")[
                            :REVIEW_COUNT
                            ]
        kwargs["reviews_count"] = kwargs["reviews"].count()
        student = getattr(self.request.user, "student", None)
        kwargs["enrollment_form"] = forms.EnrollmentCreateForm(
            initial={"course": self.object, "student": student},
        )
        enrollment = models.Enrollment.objects.filter(
            course=self.object, student=student
        ).first()
        kwargs["enrollment_accepted"] = getattr(enrollment, "accepted", "not_existing")

        return super().get_context_data(**kwargs)


class ProfessorDetailView(DetailView):
    model = Professor
    template_name = "institut/professor_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        professor_pk = self.kwargs.get("pk")
        kwargs["professor"] = get_object_or_404(Professor, pk=professor_pk)
        kwargs["reviews"] = Review.objects.filter(professor=professor_pk).order_by("-id")[
                            :REVIEW_COUNT
                            ]

        kwargs["reviews_count"] = kwargs["reviews"].count()

        object_list = models.Course.objects.created_by(professor=professor_pk)
        return super(ProfessorDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )


class CourseSearchView(FormView):
    model = models.Course
    template_name = "institut/course_search.html"
    form_class = forms.CourseSearchForm
    success_url = reverse_lazy("institut:search")
    # print(make_password('st038'))

    def get_context_data(self, **kwargs):
        object_list = self.model.objects.all().order_by('-id')[:6]
        return super(CourseSearchView, self).get_context_data(
            object_list=object_list, **kwargs
        )


class CourseSearchResultsView(FilterView):
    filterset_class = filters.CourseFilter
    template_name = "institut/course_search_results.html"
    paginate_by = 10


class HandoutListView(LoginRequiredMixin, ListView):
    model = models.Handout
    template_name = "institut/handout_list.html"

    def get_queryset(self):
        course_pk = self.kwargs.get("course_pk")
        course = get_object_or_404(models.Course, pk=course_pk)
        object_list = self.model.objects.filter(course=course).order_by("section")
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_pk = self.kwargs.get("course_pk")
        context["course"] = get_object_or_404(models.Course, pk=course_pk)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_student:
            course_pk = self.kwargs.get("course_pk")
            course = get_object_or_404(models.Course, pk=course_pk)
            student = self.request.user.student
            enrollment = models.Enrollment.objects.filter(
                course=course, student=student
            ).first()
            has_access = getattr(enrollment, "accepted", False)
            if not has_access:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HandoutUpdateView(ProfessorRequiredMixin, UpdateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "institut/handout_edit.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("institut:handouts:list", kwargs={"course_pk": course.pk})


class HandoutDeleteView(ProfessorRequiredMixin, DeleteView):
    model = models.Handout
    template_name = "confirm_delete.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("institut:handouts:list", kwargs={"course_pk": course.pk})


class HandoutCreateView(ProfessorRequiredMixin, CreateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "institut/handout_edit.html"

    def form_valid(self, form):
        course_pk = self.kwargs.get("course_pk")
        form.instance.course = get_object_or_404(models.Course, pk=course_pk)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        course_pk = self.kwargs.get("course_pk")
        return reverse("institut:handouts:list", kwargs={"course_pk": course_pk})


class EnrollmentUpdateStatusView(ProfessorRequiredMixin, JsonFormMixin, UpdateView):
    model = models.Enrollment
    fields = ["accepted"]


class EnrollmentCreateView(LoginRequiredMixin, JsonFormMixin, CreateView):
    model = models.Enrollment
    form_class = forms.EnrollmentCreateForm


class EnrollmentDeleteView(ProfessorRequiredMixin, DeleteView):
    model = models.Enrollment
    success_url = reverse_lazy("institut:list")
    template_name = "confirm_delete.html"

    # def get_success_url(self):
    #     course_pk = self.kwargs.get("course_pk")
    #     print(course_pk)
    #     return reverse("institut:enrollments:professor_Alist", kwargs={"course_pk": course_pk})


class EnrollmentStudentListView(StudentRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "institut/enrollment_list.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(
            student=self.request.user.student, accepted=True
        )
        # print(object_list)
        return object_list


class EnrollmentProfessorListView(ProfessorRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "institut/enrollment_list.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(
            course__professor=self.request.user.professor
        ).order_by("accepted")
        return object_list


class NaEnrollmentProfessorListView(ProfessorRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "institut/enrollment_list.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(Q(
            course__professor=self.request.user.professor) & Q(accepted__isnull=True)
                                                )
        return object_list


class AcEnrollmentProfessorListView(ProfessorRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "institut/enrollment_list.html"

    def get_queryset(self):
        coursex = get_object_or_404(models.Course, pk=self.kwargs.get("pk"))

        object_list = self.model.objects.filter(Q(
            course__professor=self.request.user.professor) & Q(course=coursex) & Q(accepted__isnull=False)
                                                )
        return object_list


# ********************************************************************************
# ***************** OLD Views ****************************************************
# ********************************************************************************

