from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from . import models
from opencourse.profiles.models import Student
from django.db.models import Q


class CourseForm(forms.ModelForm):
    classe = forms.ModelChoiceField(
        models.Classe.objects.all(), label=_("Class"), required=False
    )

    class Meta:
        model = models.Course
        fields = [
            "professor",
            "title",
            "credit",
            "classe",
            "area",
            "descrip",
            "extrainfo",
            "textbook",
            "picture",
            "syllabus",
            "language",
            "number_sessions",
            "active",

        ]
        labels = {
            "professor": _("Professor"),
            "title": _("Title"),
            "credit": _("Number of Credits"),
            "classe": _("Class"),
            "area": _("Area"),
            "descrip": _("Description"),
            "extrainfo": _("Extra information"),
            "textbook": _("TextBook"),
            "picture": _("Course Picture"),
            "syllabus": _("Syllabus"),
            "language": _("Language"),
            "number_sessions": _("Number of Sessions"),
            "active": _("Is this course Active?"),
        }
        widgets = {"title": forms.TextInput(attrs={"class": "maxlength-options"}),
                   "descrip": forms.Textarea(attrs={"rows": 1, "cols": 4, "class": "elastic"}),
                   "extrainfo": forms.TextInput(attrs={"class": "maxlength-options"}),
                   "textbook": forms.TextInput(attrs={"class": "maxlength-options"}),
                   "active": forms.CheckboxInput(
                       attrs={"class": "form-check-input-styled-primary"}),
                   }

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop("professor", None)
        super(CourseForm, self).__init__(*args, **kwargs)


class CourseSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = "form-field"

    city = forms.ModelChoiceField(
        models.City.objects.order_by("name"), empty_label=_("City"), required=False
    )
    area = forms.ModelChoiceField(
        models.Coursearea.objects.order_by("name"), empty_label=_("Search an Area or a Course"), required=True
    )
    name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": _("Center name")})
    )


# class CourseLocationForm(forms.ModelForm):
#     currency = forms.ModelChoiceField(
#         models.Currency.objects.all(), label=_("Currency")
#     )
#
#     class Meta:
#         model = models.CourseLocation
#         fields = ("location_type", "price", "currency")
#         labels = {
#             "location_type": _("Location type"),
#             "price": _("Price"),
#         }
#
#
# CourseLocationFormset = inlineformset_factory(
#     models.Course, models.CourseLocation, form=CourseLocationForm, extra=1,
# )


class EnrollmentView(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = [
            "accepted",
        ]
        labels = {
            "accepted": _("accepted"),
        }


class HandoutForm(forms.ModelForm):
    class Meta:
        model = models.Handout
        fields = [
            "name",
            "section",
            "description",
            "attachment",
            "link",
        ]
        labels = {
            "name": _("Name"),
            "section": _("Section"),
            "description": _("Description"),
            "attachment": _("Attachment"),
            "link": _("Youtube Link"),
        }


class EnrollmentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = ["id", "classe", "student"]


class CenterForm(forms.ModelForm):
    schoolgroup = forms.ModelChoiceField(
        models.Schoolgroup.objects.all(), label=_("School Group"), required=False
    )
    class Meta:
        model = models.Center
        fields = [
            "schoolgroup",
            "name",
            "shortname",
            "city",
            "description",
            "logo",
            "website",
            "address",
            "tel1",
            "tel2",
            "whatsapp",
            "email",
            "facebook",
            "twiter",
            "instagram",
            "youtube",
            "picture1",
            "picture2",
            "picture3",
            "picture4",
        ]
        labels = {
            "schoolgroup": _("School Group"),
            "name": _("Name"),
            "shortname": _("Short Name"),
            "city": _("City"),
            "description": _("Description"),
            "logo": _("Logo"),
            "website": _("Website"),
            "address": _("Address"),
            "tel1": _("Telephone 1"),
            "tel2": _("Telephone 2"),
            "whatsapp": _("Whatsapp"),
            "email": _("Email"),
            "facebook": _("Facebook"),
            "twiter": _("Twiter"),
            "instagram": _("Instagram"),
            "youtube": _("Youtube Channel"),
            "picture1": _("Picture 1"),
            "picture2": _("Picture 2"),
            "picture3": _("Picture 3"),
            "picture4": _("Picture 4"),
        }


class JoinRequestCreateForm(forms.ModelForm):
    class Meta:
        model = models.JoinRequest
        fields = ["id", "center", "professor"]


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = models.Academicyear
        fields = [
            "name",
            "startdate",
            "enddate",
        ]
        labels = {
            "name": _("Name"),
            "startdate": _("Start Date"),
            "enddate": _("End Date"),
        }
        widgets = {"startdate": forms.DateInput(attrs={"type": "date"}),
                   "enddate": forms.DateInput(attrs={"type": "date"})}


class HolidaysForm(forms.ModelForm):
    academicyear = forms.ModelChoiceField(
        models.Academicyear.objects.all(), label=_("Academic Year"), required=False
    )
    class Meta:
        model = models.Holidays
        fields = [
            "name",
            "academicyear",
            "startdate",
            "enddate",
            "type",
        ]
        labels = {
            "name": _("Name"),
            "academicyear": _("Academic Year"),
            "startdate": _("Start Date"),
            "enddate": _("End Date"),
            "type": _("Holiday Type"),
        }
        widgets = {"startdate": forms.DateInput(attrs={"type": "date"}),
                   "enddate": forms.DateInput(attrs={"type": "date"})}


class CourseareaForm(forms.ModelForm):
    class Meta:
        model = models.Coursearea
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }


class SchoolgroupForm(forms.ModelForm):
    class Meta:
        model = models.Schoolgroup
        fields = [
            "name",
            "shortname",
            "description",
            "logo",
            "website",
            "address",
            "tel",
            "whatsapp",
            "email",
            "facebook",
            "twiter",
            "instagram",
            "youtube",
        ]
        labels = {
            "name": _("Name"),
            "shortname": _("Short Name"),
            "description": _("Description"),
            "logo": _("Logo"),
            "website": _("Website"),
            "address": _("Address"),
            "tel": _("Tel"),
            "whatsapp": _("Whatsapp"),
            "email": _("Email"),
            "facebook": _("Facebook"),
            "twiter": _("Twiter"),
            "instagram": _("Instagram"),
            "youtube": _("Youtube"),
        }


class CenterlevelForm(forms.ModelForm):
    center = forms.ModelChoiceField(
        models.Center.objects.all(), label=_("School"), required=False
    )
    class Meta:
        model = models.Centerlevel
        fields = [
            "center",
            "name",
            "description",
        ]
        labels = {
            "center": _("School"),
            "name": _("Name"),
            "description": _("Description"),
        }


class GradeForm(forms.ModelForm):
    centerlevel = forms.ModelChoiceField(
        models.Centerlevel.objects.all(), label=_("School Level"), required=False
    )
    class Meta:
        model = models.Grade
        fields = [
            "centerlevel",
            "name",
            "description",
        ]
        labels = {
            "centerlevel": _("School Level"),
            "name": _("Name"),
            "description": _("Description"),
        }


class ClasseForm(forms.ModelForm):
    grade = forms.ModelChoiceField(
        models.Grade.objects.all(), label=_("Grade"), required=False
    )
    class Meta:
        model = models.Classe
        fields = [

            "name",
            "grade",
            "section",
            "description",
            "active",
            "allow_comments",
        ]
        labels = {

            "name": _("Name"),
            "grade": _("Grade"),
            "section": _("Section"),
            "description": _("Description"),
            "active": _("Active"),
            "allow_comments": _("Allow comments"),
        }
        widgets = {"name": forms.Textarea(attrs={"rows": 1, "cols": 20, "class": "elastic"}),
                   "description": forms.Textarea(attrs={"rows": 1, "cols": 6, "class": "elastic"}),
                   "section": forms.Textarea(attrs={"rows": 1, "cols": 2, "class": "elastic"}),
                   "active": forms.CheckboxInput(attrs={"class": "form-check-input-styled"}),
                   "allow_comments": forms.CheckboxInput(attrs={"class": "form-check-input-styled"})
                   }


class ClasseEditForm(ClasseForm):
    academicyear = forms.ModelChoiceField(
        models.Academicyear.objects.all(), label=_("Academic Year"), required=False
    )
    grade = forms.ModelChoiceField(
        models.Grade.objects.all(), label=_("Grade"), required=False
    )

    class Meta:
        model = models.Classe
        fields = [

            "name",
            "grade",
            "section",
            "academicyear",
            "description",
            "active",
            "allow_comments",
        ]
        labels = {

            "name": _("Name"),
            "grade": _("Grade"),
            "section": _("Section"),
            "academicyear": _("Academic Year"),
            "description": _("Description"),
            "active": _("Active"),
            "allow_comments": _("Allow comments"),
        }
        widgets = {"name": forms.Textarea(attrs={"rows": 1, "cols": 20, "class": "elastic"}),
                   "description": forms.Textarea(attrs={"rows": 1, "cols": 6, "class": "elastic"}),
                   "section": forms.Textarea(attrs={"rows": 1, "cols": 2, "class": "elastic"}),
                   "active": forms.CheckboxInput(attrs={"class": "form-check-input-styled"}),
                   "allow_comments": forms.CheckboxInput(attrs={"class": "form-check-input-styled"})
                   }


ClasseFormset = inlineformset_factory(
    models.Grade, models.Classe, form=ClasseEditForm, extra=1, can_delete=True,
)

class CourseTimeForm(forms.ModelForm):
    class Meta:
        model = models.Coursetime
        fields = [
            "name",
            "start",
            "end",
        ]
        labels = {
            "name": _("Day"),
            "start": _("Start Time"),
            "end": _("End Time"),
        }


# CourseTimeFormset = inlineformset_factory(
#     models.Course, models.Coursetime, form=CourseTimeForm, extra=1, can_delete=True,
# )


class SupplyForm(forms.ModelForm):
    class Meta:
        model = models.Supply
        fields = [
            "name",
            "description",
            "quantity",
            "required",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "quantity": _("Quantity"),
            "required": _("Required"),
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 1, "cols": 120, "class": "elastic maxlength"})}


SupplyFormset = inlineformset_factory(
    models.Course, models.Supply, form=SupplyForm, extra=1, can_delete=True,
)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ["subject",  "text"]
        labels = {
            "subject": _("Subject"),
            "text": _("Text"),
        }

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop("admin", None)
        #professor = admin.professor
        #print(professor)
        super(NotificationForm, self).__init__(*args, **kwargs)


class ParentNotificationForm(forms.ModelForm):
    class Meta:
        model = models.ParentNotification
        fields = ["course", "text"]
        labels = {
            "course": _("Course"),
            "text": _("Text"),
            #"student": _("Student")
        }
        #widgets = {"student": forms.Select(attrs={"class": "select-minimum"})}

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop("admin", None)
        professor = admin.professor
        #print(professor)
        super(ParentNotificationForm, self).__init__(*args, **kwargs)

        if professor:
            self.fields["course"].queryset = models.Course.objects.filter(professor=professor)
            # self.fields["student"].queryset = Student.objects.none()
            # print("intitalize the form")
            # print(self.data.get('course'))
            # if 'course' in self.data:
            #     try:
            #         course_id = int(self.data.get('course'))
            #
            #         course = models.Course.objects.filter(pk=course_id).first()
            #         classe = models.Classe.objects.filter(course=course).first()
            #         print("course_id form1:")
            #         print(course_id)
            #         self.fields["student"].queryset = Student.objects.filter(classe=classe).order_by("id")
            #         print("course_id form2:")
            #         print(course_id)
            #     except (ValueError, TypeError):
            #         pass



class CourseOutlineForm(forms.ModelForm):
    class Meta:
        model = models.CourseOutline
        fields = ["name", "description", "datedue"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "datedue": _("Date due"),
        }
        widgets = {"datedue": forms.DateInput(attrs={"type": "date"}),}


