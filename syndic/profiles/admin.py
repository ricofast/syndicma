from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from . import models


class StudentResource(resources.ModelResource):

    class Meta:
        model = models.Student


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource



class UserResource(resources.ModelResource):

    class Meta:
        model = models.User
        exclude = ('last_login', 'date_joined',)


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


admin.site.register(models.User, UserAdmin)

admin.site.register(models.Student, StudentAdmin)




model_objects = (
    models.Professor,
    models.Review,
    models.Superadmin,
    models.Regadmin,
    models.Parent,
    models.LoggedInUser
    )

for m in model_objects:
    admin.site.register(m)
