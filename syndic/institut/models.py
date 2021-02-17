from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import datetime
from django.utils.formats import date_format
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from . import managers
from opencourse.profiles.models import Professor, Student, Regadmin, Superadmin, User
from .formatChecker import ContentTypeRestrictedFileField
from embed_video.fields import EmbedVideoField
from django.urls import reverse

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'schools_pics/school_{0}/{1}'.format(instance.id, filename)


class City(models.Model):
    codepostal = models.CharField(max_length=8, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    category_1 = models.SmallIntegerField(blank=True, null=True)
    category_2 = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return str(self.name)


# class StudiesLevel(models.Model):
#     name = models.CharField(max_length=30, blank=True, null=True)
#     description = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         verbose_name = _("StudiesLevel")
#         verbose_name_plural = _("StudiesLevels")
#
#     def __str__(self):
#         return str(self.name)


class Academicyear(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    term = models.CharField(max_length=50, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _("Academicyear")
        verbose_name_plural = _("Academicyears")
        permissions = (("manage_academicyear", _("Manage academicyear")),)

    def __str__(self):
        return str(self.name)


class Holidays(models.Model):
    typebreak = (
        ('NH', _("National Holiday")),
        ('RH', _("Religious Holiday")),
        ('SB', _("School Break")),
    )
    academicyear = models.ForeignKey(Academicyear, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=2, choices=typebreak)

    class Meta:
        verbose_name = _("Holidays")
        verbose_name_plural = _("Holidays")
        permissions = (("manage_holidays", _("Manage holidays")),)

    def __str__(self):
        return str(self.name)


class Coursearea(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return str(self.name)


class CourseLanguage(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    tag = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return str(self.name)


class Schoolgroup(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    shortname = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=60, blank=True, null=True)
    twiter = models.CharField(max_length=60, blank=True, null=True)
    instagram = models.CharField(max_length=60, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    logo = models.FileField(upload_to="schools_pics/logos/",
                            validators=[FileExtensionValidator(['jpeg', 'bmp', 'svg', 'gif', 'png', 'ico'])],
                            blank=True, null=True)
    # logo = ContentTypeRestrictedFileField(upload_to=user_directory_path,
    #                                       content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png',
    #                                                      'application/svg', ],
    #                                       max_upload_size=1048576, blank=True, null=True)


    class Meta:
        verbose_name = _("Schoolgroup")
        verbose_name_plural = _("Schoolgroups")
        permissions = (("manage_schoolgroup", _("Manage schoolgroup")),)

    def __str__(self):
        return str(self.name)


class Center(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    schoolgroup = models.ForeignKey(Schoolgroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40)
    shortname = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    tel1 = models.CharField(max_length=20, blank=True, null=True)
    tel2 = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=60, blank=True, null=True)
    twiter = models.CharField(max_length=60, blank=True, null=True)
    instagram = models.CharField(max_length=60, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    logo = models.FileField(upload_to="schools_pics/logos/",
                            validators=[FileExtensionValidator(['jpg', 'bmp', 'svg', 'gif', 'png', 'ico'])],
                            blank=True, null=True)
    picture1 = ContentTypeRestrictedFileField(upload_to=user_directory_path,
                                              content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ],
                                              max_upload_size=1048576, blank=True, null=True)
    picture2 = ContentTypeRestrictedFileField(upload_to=user_directory_path,
                                              content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ],
                                              max_upload_size=1048576, blank=True, null=True)
    picture3 = ContentTypeRestrictedFileField(upload_to=user_directory_path,
                                              content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ],
                                              max_upload_size=1048576, blank=True, null=True)
    picture4 = ContentTypeRestrictedFileField(upload_to=user_directory_path,
                                              content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ],
                                              max_upload_size=1048576, blank=True, null=True)
    created = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Center")
        verbose_name_plural = _("Centers")
        permissions = (("manage_center", _("Manage center")),)

    def __str__(self):
        return str(self.name)


class Centerlevel(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=255, blank=True, null=True)


    class Meta:
        verbose_name = _("Centerlevel")
        verbose_name_plural = _("Centerlevels")
        permissions = (("manage_centerlevel", _("Manage center level")),)

    def __str__(self):
        return str(self.name)


class Grade(models.Model):
    centerlevel = models.ForeignKey(Centerlevel, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=255, blank=True, null=True)


    class Meta:
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")
        permissions = (("manage_grade", _("Manage grade")),)

    def __str__(self):
        return str(self.name)


class Classe(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    academicyear = models.ForeignKey(Academicyear, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)
    section = models.CharField(max_length=2, blank=True, null=True)
    student = models.ManyToManyField(Student)
    allow_comments = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Classe")
        verbose_name_plural = _("Classes")
        permissions = (("manage_classe", _("Manage classe")),)

    def get_absolute_url(self):
        return reverse('institut:profclasse', args=[str(self.pk)])

    def __str__(self):
        return str(self.name)


class Course(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=65)
    descrip = models.TextField(blank=True)
    extrainfo = models.CharField(max_length=250, blank=True, null=True)
    textbook = models.CharField(max_length=100, blank=True, null=True)
    credit = models.SmallIntegerField(blank=True, null=True)
    number_sessions = models.SmallIntegerField(blank=True, null=True)
    area = models.ManyToManyField(Coursearea)
    language = models.ManyToManyField(CourseLanguage)
    picture = ContentTypeRestrictedFileField(upload_to="course_pics/%Y-%m-%d/",
                                             content_types=['image/bmp', 'image/gif', 'image/jpeg', 'image/png', ],
                                             max_upload_size=1048576, blank=True, null=True)
    syllabus = ContentTypeRestrictedFileField(upload_to="handouts/%Y-%m-%d/",
                                              content_types=['application/docx', 'application/pdf', 'application/doc',
                                                             'application/xlsx', 'application/xls', 'application/pptx',
                                                             'application/ppt', 'image/jpeg', 'image/png', ],
                                              max_upload_size=2621440, blank=True, null=True)
    private = models.BooleanField(default=True)
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    objects = managers.CourseManager()

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        permissions = (("manage_course", _("Manage course")),)

    def __str__(self):
        return self.title or ""


class Coursetime(models.Model):
    cdays = (
        ('Mo', _("Monday")),
        ('Tu', _("Tuesday")),
        ('We', _("Wednesday")),
        ('Th', _("Thursday")),
        ('Fr', _("Friday")),
        ('Sa', _("Saturday")),
        ('Su', _("Sunday")),
    )
    times = (
        ('08:00', ("08:00")),
        ('08:30', ("08:30")),
        ('09:00', ("09:00")),
        ('09:30', ("09:30")),
        ('10:00', ("10:00")),
        ('10:30', ("10:30")),
        ('11:00', ("11:00")),
        ('11:30', ("11:30")),
        ('12:00', ("12:00")),
        ('12:30', ("12:30")),
        ('13:00', ("13:00")),
        ('13:30', ("13:30")),
        ('14:00', ("14:00")),
        ('14:30', ("14:30")),
        ('15:00', ("15:00")),
        ('15:30', ("15:30")),
        ('16:00', ("16:00")),
        ('16:30', ("16:30")),
        ('17:00', ("17:00")),
        ('17:30', ("17:30")),
        ('18:00', ("18:00")),
        ('18:30', ("18:30")),
        ('19:00', ("19:00")),
        ('19:30', ("19:30")),
        ('20:00', ("20:00")),
        ('20:30', ("20:30")),
        ('21:00', ("21:00")),
        ('21:30', ("21:30")),
        ('22:00', ("22:00")),
        ('22:30', ("22:30")),

    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=10, null=True, blank=True)
    courseday = models.SmallIntegerField(null=True, blank=True)
    starttime = models.TimeField(null=True, blank=True)
    endtime = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Coursetime")
        verbose_name_plural = _("Coursetimes")
        permissions = (("manage_coursetime", _("Manage course time")),)

    # def save(self, *args, **kwargs):
    #      ntime = self.start
    #      self.starttime = ntime.time
    #      super(Coursetime, self).save(*args, **kwargs)

    def __str__(self):
        return "{}({}-{})".format(self.name, self.starttime, self.endtime)


class Attendance(models.Model):
    Attendance_State = (
        ('P', _("Present")),
        ('E', _("Excused Absence")),
        ('U', _("Unexcused Absence")),
        ('L', _("Late")),
    )
    coursetime = models.ForeignKey(Coursetime, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendancedate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=Attendance_State)

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
        permissions = (("manage_attendance", _("Manage attendance")),)

    def __str__(self):
        return "{}: {}".format(self.student, self.status)


class Supply(models.Model):
    Supply_type = (
        ('Bo', _("Book")),
        ('No', _("Notebook")),
        ('Pe', _("Ballpoint pens")),
        ('Pc', _("Pencil")),
        ('Co', _("Cover")),
        ('Ru', _("Ruler")),
        ('Er', _("Erasers")),
        ('Bi', _("3-ring binder")),
        ('Sh', _("Sharpeners")),
        ('Hi', _("Highlighters")),
        ('Ma', _("Markers")),
        ('Gl', _("Glue Sticks")),
        ('Wp', _("Watercolor paints")),
        ('Cp', _("Colored pencils")),
        ('Fo', _("Folder")),
        ('Ti', _("Box of tissues")),
        ('Sc', _("Scissors")),
        ('Dp', _("Drawing Paper")),
        ('Ag', _("Agenda")),
        ('Sl', _("Slate")),
        ('Wp', _("White Paper Ram")),
        ('Ca', _("pencil case")),
        ('Cs', _("Compass")),
        ('Pr', _("Protractor")),
        ('Sq', _("Set Square")),
        ('Di', _("Dictionary")),
        ('Ot', _("Other")),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=2, choices=Supply_type)
    description = models.TextField(max_length=100, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    required = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Supply")
        verbose_name_plural = _("Supplies")

    def __str__(self):
        return "{}: {}".format(self.course, self.name)


class Enrollment(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True)
    accepted = models.NullBooleanField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = managers.EnrollmentManager()

    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollment")
        permissions = (("manage_enrollment", _("Manage enrollment")),)
        unique_together = ("classe", "student")

    def __str__(self):
        return "{}: {} ({})".format(self.classe, self.student, self.accepted)


class HandoutSection(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)


class Handout(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=1000, blank=True, null=True)
    link = EmbedVideoField(blank=True, null=True)  # same like models.URLField()
    attachment = ContentTypeRestrictedFileField(upload_to="handouts/%Y-%m-%d/",
                                                content_types=['application/docx', 'application/pdf', 'application/doc',
                                                               'application/xlsx', 'application/xls',
                                                               'application/pptx', 'application/ppt', 'image/jpeg',
                                                               'image/png', ], max_upload_size=2621440, blank=True,
                                                null=True)
    section = models.ForeignKey(HandoutSection, on_delete=models.PROTECT)

    objects = managers.HandoutManager()

    class Meta:
        verbose_name = _("Handout")
        verbose_name_plural = _("Handout")
        permissions = (("manage_handout", _("Manage handout")),)

    def __str__(self):
        return str(self.name)


class JoinRequest(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    accepted = models.NullBooleanField()

    objects = managers.JoinRequestManager()

    class Meta:
        verbose_name = _("Join request")
        verbose_name_plural = _("Join requests")
        permissions = (("manage_join_request", _("Manage join request")),)
        unique_together = ("center", "professor")

    def __str__(self):
        return "{}: {} ({})".format(self.center, self.professor, self.accepted)


class Notification(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    #classe = models.ForeignKey(Classe, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=250, blank=True, null=True)
    # attachment = ContentTypeRestrictedFileField(upload_to="handouts/%Y-%m-%d/",
    #                                             content_types=['application/docx', 'application/pdf', 'application/doc',
    #                                                            'application/xlsx', 'application/xls',
    #                                                            'application/pptx', 'application/ppt', 'image/jpeg',
    #                                                            'image/png', ], max_upload_size=2621440, blank=True,
    #                                             null=True)
    parentread = models.BooleanField(default=False)
    studentread = models.BooleanField(default=False)
    notifydate = models.DateTimeField(default=datetime.now())
    readdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.subject


class NotificationLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=250, blank=True, null=True)
    notifydate = models.DateTimeField(default=datetime.now())


    class Meta:
        verbose_name = _("NotificationLog")
        verbose_name_plural = _("NotificationLogs")

    def __str__(self):
        return self.subject


class ParentNotification(models.Model):
    Notice_type = (
        ('G', _("Grade")),
        ('A', _("Attendance")),
        ('O', _("Course Outline")),
        ('W', _("Course Work")),
        ('M', _("Message"))

    )
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=250)
    parentread = models.BooleanField(default=False)
    studentread = models.BooleanField(default=False)
    student = models.ManyToManyField(Student, blank=True, null=True)
    notifydate = models.DateTimeField(default=datetime.now())
    readdate = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=Notice_type, blank=True, null=True)
    typeid = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = _("ParentNotification")
        verbose_name_plural = _("ParentNotifications")

    def __str__(self):
        return str(self.text)


class CourseGrades(models.Model):
    admin = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    grade = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _("CourseGrades")
        verbose_name_plural = _("CourseGrades")
        permissions = (("manage_coursegrades", _("Manage Course_Grades")),)

    def __str__(self):
        return self.name


class CourseWork(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    dateposted = models.DateTimeField(auto_now=True, blank=True, null=True)
    datedue = models.DateTimeField(blank=True, null=True)
    weekdue = models.SmallIntegerField(blank=True, null=True)
    graded = models.NullBooleanField(blank=True, null=True)
    document = ContentTypeRestrictedFileField(upload_to="handouts/%Y-%m-%d/",
                                              content_types=['application/docx', 'application/pdf', 'application/doc',
                                                             'application/xlsx', 'application/xls',
                                                             'application/pptx', 'application/ppt', 'image/jpeg',
                                                             'image/png', ], max_upload_size=2621440, blank=True,
                                              null=True)

    class Meta:
        verbose_name = _("CourseWork")
        verbose_name_plural = _("CourseWork")
        permissions = (("manage_coursework", _("Manage Course_Work")),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
         ntime = self.datedue
         self.weekdue = date_format(ntime, 'W')
         super(CourseWork, self).save(*args, **kwargs)


class CourseOutline(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    datedue = models.DateTimeField(blank=True, null=True)
    weekdue = models.SmallIntegerField(blank=True, null=True)
    document = ContentTypeRestrictedFileField(upload_to="handouts/%Y-%m-%d/",
                                              content_types=['application/docx', 'application/pdf', 'application/doc',
                                                             'application/xlsx', 'application/xls',
                                                             'application/pptx', 'application/ppt', 'image/jpeg',
                                                             'image/png', ], max_upload_size=2621440, blank=True,
                                              null=True)

    class Meta:
        verbose_name = _("CourseOutline")
        verbose_name_plural = _("CourseOutline")
        permissions = (("manage_courseoutline", _("Manage Course_Outline")),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ntime = self.datedue
        self.weekdue = date_format(ntime, 'W')
        super(CourseOutline, self).save(*args, **kwargs)


class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

