from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import GuardianUserMixin
from datetime import datetime
from .formatChecker import ContentTypeRestrictedFileField
#from opencourse.institut.models import Academicyear

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile_pics/user_{0}/{1}'.format(instance.user.id, filename)

class User(GuardianUserMixin, AbstractUser):
    passchanged = models.NullBooleanField(default=False)
    @property
    def profile(self):
        if hasattr(self, "professor"):
            return self.professor
        elif hasattr(self, "student"):
            return self.student
        elif hasattr(self, "parent"):
            return self.parent
        elif hasattr(self, "superadmin"):
            return self.superadmin
        elif hasattr(self, "regadmin"):
            return self.regadmin
        else:
            return self

    @property
    def is_student(self):
        return hasattr(self, "student")

    @property
    def is_regadmin(self):
        return hasattr(self, "regadmin")

    @property
    def is_superadmin(self):
        return hasattr(self, "superadmin")

    @property
    def is_parent(self):
        return hasattr(self, "parent")

    @property
    def is_professor(self):
        return hasattr(self, "professor")

    class Meta(AbstractUser.Meta):
        permissions = (
            ("access_professor_pages", _("Access professor pages")),
            ("access_student_pages", _("Access student pages")),
            ("access_regadmin_pages", _("Access regular admin pages")),
            ("access_superadmin_pages", _("Access super admin pages")),
            ("access_parent_pages", _("Access parent pages")),
        )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = ContentTypeRestrictedFileField(_("Profile picture"), upload_to=user_directory_path, content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ], max_upload_size=1048576, blank=True, null=True)
    picture1 = ContentTypeRestrictedFileField(_("Profile picture1"), upload_to=user_directory_path, content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ], max_upload_size=1048576, blank=True, null=True)
    picture2 = ContentTypeRestrictedFileField(_("Profile picture2"), upload_to=user_directory_path, content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ], max_upload_size=1048576, blank=True, null=True)
    email_verified = models.BooleanField(_("Email verified"), default=False)

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    edulevel = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    dateadd = models.DateField(blank=True, null=True, default=datetime.now())
    contacts_requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.user.first_name:
            return "{} - {}".format(self.user.first_name, self.user.last_name)
        return self.user.username

    class Meta:
        abstract = True


class Parent(Profile):
    parentallink = models.CharField(max_length=20, blank=True, null=True)
    active = models.NullBooleanField(default=False)

    class Meta(Profile.Meta):
        verbose_name = _("Parent")
        verbose_name_plural = _("Parents")


class Student(Profile):
    parent = models.ForeignKey(Parent, on_delete=models.PROTECT, blank=True, null=True)
    code = models.CharField(max_length=15, unique=True, blank=True, null=True)

    class Meta(Profile.Meta):
        verbose_name = _("Student")
        verbose_name_plural = _("Students")


class Professor(Profile):
    code = models.CharField(max_length=15, unique=True, blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    experience = models.TextField(max_length=1000, blank=True, null=True)
    yearsexperience = models.SmallIntegerField(blank=True, null=True)
    act_position = models.CharField(max_length=100, blank=True, null=True)
    dateexpir = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(default=False)
    feespaid = models.NullBooleanField()

    class Meta(Profile.Meta):
        verbose_name = _("Professor")
        verbose_name_plural = _("Professors")

    @property
    def average_score(self):
        reviews = self.review_set.all()
        score = reviews.aggregate(models.Avg("score"))["score__avg"]
        return score


class Superadmin(Profile):
    bio = models.TextField(max_length=1000, blank=True, null=True)
    yearsexperience = models.SmallIntegerField(blank=True, null=True)
    act_position = models.CharField(max_length=100, blank=True, null=True)
    dateexpir = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(default=True)


    class Meta(Profile.Meta):
        verbose_name = _("Superadmin")
        verbose_name_plural = _("Superadmins")


class Regadmin(Profile):
    bio = models.TextField(max_length=1000, blank=True, null=True)
    yearsexperience = models.SmallIntegerField(blank=True, null=True)
    act_position = models.CharField(max_length=100, blank=True, null=True)
    dateexpir = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(default=False)

    class Meta(Profile.Meta):
        verbose_name = _("Regadmin")
        verbose_name_plural = _("Regadmins")


class Review(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    text = models.TextField()
    coursename = models.CharField(max_length=100)
    reviewdate = models.DateTimeField(blank=True, null=True, default=datetime.now())

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author = GenericForeignKey("content_type", "author_id")

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.text


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="logged_in_user", on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    # academicyear = models.ForeignKey(Student, on_delete=models.PROTECT, blank=True, null=True)
    # studentpk = models.ForeignKey(Academicyear, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.user.first_name