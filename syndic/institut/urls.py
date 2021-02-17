from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

app_name = "institut"

course_patterns = [
    url('^calendar', views.calendar, name='calendar'),
    url('^add_event$', views.AddeventView.as_view(), name='add_event'),
    url('^update$', views.UpdateeventView.as_view(), name='update'),
    url('^remove', views.remove, name='remove'),
    path("list/", views.CourseListView.as_view(), name="list"),
    path("firebase/", views.FirebaseView.as_view(), name="firebase"),
    path("create/<int:classe_pk>/", views.CourseCreateView.as_view(), name="create"),
    path("editcalender/<int:pk>/", views.CalenderEditView.as_view(), name="calenderedit"),
    path("profcalender/<int:prof_pk>/", views.ProfCalenderView.as_view(), name="profcalender"),
    path("studentcalender/<int:student_pk>/", views.StudentCalenderView.as_view(), name="studentcalender"),
    path("agenda/<int:classe_pk>/", views.AgendaCalenderView.as_view(), name="agenda"),
    path("classcalender/<int:classe_pk>/", views.ClasseCalenderView.as_view(), name="classcalender"),
    path("detail/<int:pk>/", views.CourseDetailView.as_view(), name="detail"),
    path("profdetail/<int:pk>/", views.ProfessorDetailView.as_view(), name="profdetail"),
    path("edit/<int:pk>/", views.CourseEditView.as_view(), name="edit"),
    path("editadmin/<int:pk>/", views.CourseEdittimeView.as_view(), name="edittime"),
    path("delete/<int:pk>/", views.CourseDeleteView.as_view(), name="delete"),
    path("search/", views.CourseSearchView.as_view(), name="search"),
    path("grade/create/", views.GradeCreateView.as_view(), name="gradecreate"),
    path("grade/edit/<int:pk>/", views.GradeEditeView.as_view(), name="gradeedit"),
    path("grade/list/", views.GradeListView.as_view(), name="gradelist"),
    path("grade/delete/<int:pk>/", views.GradeDeleteView.as_view(), name="gradedelete"),
    path("courseoutline/create/<int:course_pk>/", views.CourseOutlineCreateView.as_view(), name="courseoutline_create"),
    path("courseoutline/edit/<int:pk>/", views.CourseOutlineEditView.as_view(), name="courseoutline_edit"),
    path("courseoutline/list/<int:course_pk>/", views.CourseOutlineListView.as_view(), name="courseoutline_list"),
    path("courseoutline/delete/<int:pk>/", views.CourseOutlineDeleteView.as_view(), name="courseoutline_delete"),
    path("class/create/", views.ClasseCreateView.as_view(), name="classcreate"),
    path("class/edit/<int:pk>/", views.ClasseEditeView.as_view(), name="classedit"),
    path("class/list/", views.ClasseListView.as_view(), name="classlist"),
    path("class/proflist/", views.ClasseProfListView.as_view(), name="classproflist"),
    path("class/delete/<int:pk>/", views.ClasseDeleteView.as_view(), name="classdelete"),
    path("academicyear/<int:pk>/", views.AcademicyearEditView.as_view(), name="academicyear_edit"),
    path("attendance/<int:coursetime_pk>/<str:at_date>/", views.AttendanceView.as_view(), name="attendance"),
    path("attendances/<int:student_pk>/", views.AttendanceListView.as_view(), name="prattendance"),
    url('^add_attendance$', views.AttendanceCreateView.as_view(), name='add_attendance'),
    path("profdashboard/", views.ProfessorDashboardView.as_view(), name="profdash"),
    path("dashboard/", views.StudentDashboardView.as_view(), name="dashboard"),
    path("profclasse/<int:pk>/", views.ClasseProfView.as_view(), name="profclasse"),
    path("parentnotify/", views.ParentNotifyListView.as_view(), name="parentnotifylist"),
    path("message/", views.MessageSendView.as_view(), name="message"),
    url('^deletemessage', views.deletemessage, name='deletemessage'),
    path('load_students/', views.load_students, name='load_students'),
    url('^edit_parentnotify$', views.ParentNotifyUpdateView.as_view(), name='edit_parentnotify'),
    url('^edit_kids$', views.parentkidselect, name='edit_kids'),
    url('^edit_year$', views.acayearselect, name='edit_year'),
    url('^save_message$', views.SaveMessageView.as_view(), name='save_message'),
    path("messages/list/", views.MessagesListView.as_view(), name="messages_list"),
    path(
        "<int:pk>/students/",
        views.CourseStudentsListView.as_view(),
        name="students_list",
    ),
    path(
        "search-results/",
        views.CourseSearchResultsView.as_view(),
        name="search_results",
    ),
]

enrollment_patterns = [
    path(
        "professor/", views.EnrollmentProfessorListView.as_view(), name="professor_list"
    ),
    path(
        "professor/accepted/<int:pk>/", views.AcEnrollmentProfessorListView.as_view(), name="professor_Alist"
    ),
    path(
        "professorn/", views.NaEnrollmentProfessorListView.as_view(), name="professor_Nlist"
    ),
    path("student/", views.EnrollmentStudentListView.as_view(), name="student_list"),
    path("create", views.EnrollmentCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", views.EnrollmentDeleteView.as_view(), name="delete"),
    path("edit/<int:pk>/", views.EnrollmentUpdateStatusView.as_view(), name="edit"),
]

handout_patterns = [
    path("list/<int:course_pk>/", views.HandoutListView.as_view(), name="list"),
    path("create/<int:course_pk>/", views.HandoutCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.HandoutUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", views.HandoutDeleteView.as_view(), name="delete"),
]

center_patterns = [
    path("list/", views.CenterListView.as_view(), name="list"),
    path("create/", views.CenterCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.CenterEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", views.CenterDeleteView.as_view(), name="delete"),
    path("detail/<int:pk>/", views.CenterDetailView.as_view(), name="detail"),
    path("centerlevels/create/", views.CenterlevelCreateView.as_view(), name="centerlvl_create"),
    path("centerlevels/list/", views.CenterlevelListView.as_view(), name="centerlvl_list"),
    path("centerlevels/edit/<int:pk>/", views.CenterlevelEditView.as_view(), name="centerlvl_edit"),
    path("centerlevels/delete/<int:pk>/", views.CenterlevelEditView.as_view(), name="centerlvl_delete"),
    path(
        "search-results/",
        views.CenterSearchResultsView.as_view(),
        name="search_results",
    ),
]

schoolgroup_patterns = [
    path("list/", views.SchoolgroupListView.as_view(), name="list"),
    path("create/", views.SchoolgroupCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.SchoolgroupEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", views.SchoolgroupdeleteView.as_view(), name="delete"),
]
join_request_patterns = [
    path("admin/", views.JoinRequestrListView.as_view(), name="admin_list"),
    path("create/", views.JoinRequestCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.JoinRequestUpdateView.as_view(), name="edit"),
]

urlpatterns = [
    path("", include(course_patterns)),
    path("howto/", views.HowToView.as_view(), name="howto"),
    path("holidays/", views.HolidaysSearchResultsView.as_view(), name="holidays"),
    path("holidays/list/", views.HolidaysListView.as_view(), name="holidays_list"),
    path("holidays/create/", views.HolidaysCreateView.as_view(), name="holidays_create"),
    path("holidays/edit/<int:pk>/", views.HolidaysEditView.as_view(), name="holidays_edit"),
    path("holidays/delete/<int:pk>/", views.HolidaysDeleteView.as_view(), name="holidays_delete"),
    path(
        "enrollments/",
        include((enrollment_patterns, "opencourse.institut"), namespace="enrollments"),
    ),
    path(
        "handouts/",
        include((handout_patterns, "opencourse.institut"), namespace="handouts"),
    ),
    path(
        "schoolgroup/",
        include((schoolgroup_patterns, "opencourse.institut"), namespace="schoolgroups"),
    ),
    path(
        "centers/",
        include((center_patterns, "opencourse.institut"), namespace="centers"),
    ),
    path(
        "join_requests/",
        include(
            (join_request_patterns, "opencourse.institut"), namespace="join_requests"
        ),
    ),
]
