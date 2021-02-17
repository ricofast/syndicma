from django.db.models.signals import post_save
from .models import ParentNotification, CourseGrades, CourseWork, CourseOutline, Attendance, Course, NotificationLog, Notification
from opencourse.profiles.models import Professor, Student, Parent, User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from opencourse.profiles.models import LoggedInUser


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user= kwargs.get('user'))

@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()


# def create_notificationlog(sender, instance, created, **kwargs):
#     if created:
#         user = instance.admin.user
#         ParentNotification.objects.create(admin=user, text=instance.text, subject=instance.subject,
#                                           receiver=instance.course, student=instance.student, type="G", typeid=instance.id)


def create_coursegradenotification(sender, instance, created, **kwargs):
    if created:
        user = instance.admin.user
        ParentNotification.objects.create(admin=user, text=_("New grade"),
                                          course=instance.course, student=instance.student, type="G", typeid=instance.id)


def update_coursegradenotification(sender, instance, created, **kwargs):
    if created==False:
        user = instance.admin.user
        ParentNotification.objects.create(admin=user, text=_("Modified grade"),
                                          course=instance.course, student=instance.student, type="G", typeid=instance.id)


def create_courseworknotification(sender, instance, created, **kwargs):
    if created:
        professor = Professor.objects.filter(course=instance.course).first()
        user = professor.user
        ParentNotification.objects.create(admin=user, text=_("New Assignment"),
                                          course=instance.course, type="W", typeid=instance.id)


def update_courseworknotification(sender, instance, created, **kwargs):
    if created==False:
        professor = Professor.objects.filter(course=instance.course).first()
        user = professor.user
        ParentNotification.objects.create(admin=user, text=_("Modified Assignment"),
                                          course=instance.course, type="W", typeid=instance.id)


def create_attendancenotification(sender, instance, created, **kwargs):
    if created:
        course = Course.objects.filter(coursetime=instance.coursetime).first()
        professor = Professor.objects.filter(course=course).first()
        user = professor.user
        if instance.status == "U":
            text = _("Unexcused Absence")
        elif instance.status == "E":
            text = _("Excused Absence")
        else:
            text = _("Late")
        ParentNotification.objects.create(notifydate=instance.attendancedate, text=text,
                                          course=course, student=instance.student, admin=user, type="A", typeid=instance.id)


def update_attendancenotification(sender, instance, created, **kwargs):
    if created==False:
        if instance.status == "U":
            text = _("Unexcused Absence")
        elif instance.status == "E":
            text = _("Excused Absence")
        else:
            text = _("Late")
        ParentNotification.objects.update(text=text)


def create_courseoutlinenotification(sender, instance, created, **kwargs):
    if created:
        professor = Professor.objects.filter(course=instance.course).first()
        user = professor.user
        ParentNotification.objects.create(admin=user, text=_("New Course Outline"),
                                          course=instance.course, type="O", typeid=instance.id)


def update_courseoutlinenotification(sender, instance, created, **kwargs):
    if created==False:
        professor = Professor.objects.filter(course=instance.course).first()
        user = professor.user
        ParentNotification.objects.create(admin=user, text=_("Modified Outline"),
                                          course=instance.course, type="O", typeid=instance.id)


post_save.connect(create_coursegradenotification, sender=CourseGrades)


post_save.connect(update_coursegradenotification, sender=CourseGrades)


post_save.connect(create_courseworknotification, sender=CourseWork)


post_save.connect(update_courseworknotification, sender=CourseWork)


post_save.connect(create_attendancenotification, sender=Attendance)


post_save.connect(update_attendancenotification, sender=Attendance)


post_save.connect(create_courseoutlinenotification, sender=CourseOutline)


post_save.connect(update_courseoutlinenotification, sender=CourseOutline)
