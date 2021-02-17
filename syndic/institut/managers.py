from django.db import models


class CourseManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor, aca_year):
        return self.filter(professor=professor, classe__academicyear=aca_year)


class EnrollmentManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, student):
        return self.filter(student=student)


class HandoutManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)


# class CenterManager(models.Manager):
#     use_for_related_fields = True
#
#     def created_by(self, admin):
#         return self.filter(admin=admin)
#
#
# class AcademicyearManager(models.Manager):
#     use_for_related_fields = True
#
#     def created_by(self, admin):
#         return self.filter(admin=admin)
#
#
# class CourseGradesManager(models.Manager):
#     use_for_related_fields = True
#
#     def created_by(self, admin):
#         return self.filter(admin=admin)
#
# class HolidaysManager(models.Manager):
#     use_for_related_fields = True
#
#     def created_by(self, admin):
#         return self.filter(admin=admin)
#
#
# class GroupManager(models.Manager):
#     use_for_related_fields = True
#
#     def created_by(self, admin):
#         return self.filter(admin=admin)

class JoinRequestManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)
