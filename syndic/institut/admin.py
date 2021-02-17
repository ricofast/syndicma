from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from embed_video.admin import AdminVideoMixin
from opencourse.institut import models


#----------  Comments  --------------------------
# from django.utils.translation import ugettext_lazy as _
# from django_comments_xtd.admin import XtdCommentsAdmin
#
#
# class MyCommentAdmin(XtdCommentsAdmin):
#     list_display = ('thread_level', 'title', 'cid', 'name', 'content_type',
#                     'object_pk', 'submit_date', 'followup', 'is_public',
#                     'is_removed')
#     list_display_links = ('cid', 'title')
#     fieldsets = (
#         (None,          {'fields': ('content_type', 'object_pk', 'site')}),
#         (_('Content'),  {'fields': ('title', 'user', 'user_name', 'user_email',
#                                   'user_url', 'comment', 'followup')}),
#         (_('Metadata'), {'fields': ('submit_date', 'ip_address',
#                                     'is_public', 'is_removed')}),
#     )

# admin.site.register(models.MyComment, MyCommentAdmin)


class CourseResource(resources.ModelResource):

    class Meta:
        model = models.Course

class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
# class CourseInline(admin.TabularInline):
#     model = models.CourseLocation


# class CourseAdmin(GuardedModelAdmin):
#     inlines = [
#         CourseInline,
#     ]


admin.site.register(models.Course, CourseAdmin)

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

model_objects = (
    models.Schoolgroup,
    models.Center,
    models.Academicyear,
    models.Centerlevel,
    models.Coursearea,
    models.City,
    models.Holidays,
    models.Grade,
    models.CourseLanguage,
    models.Classe,
    models.Coursetime,
    models.Handout,
    models.Enrollment,
    models.HandoutSection,
    models.JoinRequest,
    models.Supply,
    models.CourseGrades,
    models.Events,
    models.Attendance,
    models.CourseOutline,
    models.CourseWork,
    models.ParentNotification,
    models.Notification,
    models.NotificationLog
)

for m in model_objects:
    admin.site.register(m, type(m.__name__ + "Admin", (admin.ModelAdmin,), {}))


