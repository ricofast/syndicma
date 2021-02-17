from django import forms
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import Permission, Group
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import SignupForm
from . import models


User = get_user_model()


class ProfileCreateForm(SignupForm):
    USER_TYPES = [("professor", _("Professor")), ("student", _("Student")), ("parent", _("Parent")), ("superadmin", _("SuperAdmin")), ("regadmin", _("Admin"))]
    user_type = forms.ChoiceField(choices=USER_TYPES)

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

    def save(self, request):
        with transaction.atomic():
            user = super().save(request)

            user_type = self.cleaned_data["user_type"]
            user_type_class_map = {
                "professor": models.Professor,
                "student": models.Student,
                "parent": models.Parent,
                "superadmin": models.Superadmin,
                "regadmin": models.Regadmin,
            }
            user_class = user_type_class_map[user_type]
            profile = user_class()
            setattr(user, user_type, profile)

            permission = get_object_or_404(
                Permission, codename=f"access_{user_type}_pages"
            )
            user.user_permissions.add(permission)

            group_name = f"{user_type}s".capitalize()
            group, created = Group.objects.get_or_create(name=group_name)
            print('group_name')
            print(group_name)
            print('group')
            print(group)
            user.groups.add(group)

            user.save()
            profile.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = models.Professor
        fields = [
            "tel",
            "dob",
            "city",
            "address",
            "bio",
            "edulevel",
            "experience",
            "yearsexperience",
            "picture",
            "picture1",
            "picture2",
        ]
        labels = {
            "tel": _("Telephone"),
            "dob": _("Date of birth"),
            "address": _("Address"),
            "city": _("City"),
            "bio": _("Biography"),
            "edulevel": _("Education"),
            "experience": _("Qualification / Experience"),
            "yearsexperience": _("Years of Experience"),
            "picture": _("Picture 1"),
            "picture1": _("Picture 2"),
            "picture2": _("Picture 3"),
        }
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}

class RegdminForm(forms.ModelForm):
    class Meta:
        model = models.Regadmin
        fields = [
            "tel",
            "dob",
            "city",
            "bio",
            "edulevel",
            "yearsexperience",
            "picture",
            "picture1",
            "picture2",
        ]
        labels = {
            "tel": _("Telephone"),
            "dob": _("Date of birth"),
            "city": _("City"),
            "bio": _("Biography"),
            "edulevel": _("Education level"),
            "yearsexperience": _("Years of experience"),
            "picture": _("Picture 1"),
            "picture1": _("Picture 2"),
            "picture2": _("Picture 3"),
        }
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}

class SuperadminForm(forms.ModelForm):
    class Meta:
        model = models.Superadmin
        fields = [
            "tel",
            "dob",
            "city",
            "bio",
            "edulevel",
            "yearsexperience",
            "picture",
            "picture1",
            "picture2",
        ]
        labels = {
            "tel": _("Telephone"),
            "dob": _("Date of birth"),
            "city": _("City"),
            "bio": _("Biography"),
            "edulevel": _("Education level"),
            "yearsexperience": _("Years of experience"),
            "picture": _("Picture 1"),
            "picture1": _("Picture 2"),
            "picture2": _("Picture 3"),
        }
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}


class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = [
            "tel",
            "dob",
            "city",
            "edulevel",
            "picture",
        ]
        labels = {
            "tel": _("Telephone"),
            "dob": _("Date of birth"),
            "city": _("City"),
            "edulevel": _("Education level"),
            "picture": _("Picture"),
        }
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}


class ParentForm(forms.ModelForm):
    class Meta:
        model = models.Parent
        fields = [
            "tel",
            "dob",
            "city",
            "edulevel",
            "picture",
        ]
        labels = {
            "tel": _("Telephone"),
            "dob": _("Date of birth"),
            "city": _("City"),
            "edulevel": _("Education level"),
            "picture": _("Picture"),
        }


ProfessorFormSet = inlineformset_factory(
    User, models.Professor, form=ProfessorForm, exclude=[], extra=1, can_delete=False,
)

StudentFormSet = inlineformset_factory(
    User, models.Student, form=StudentForm, exclude=[], extra=1, can_delete=False,
)

ParentFormSet = inlineformset_factory(
    User, models.Parent, form=ParentForm, exclude=[], extra=1, can_delete=False,
)

RegadminFormSet = inlineformset_factory(
    User, models.Regadmin, form=RegdminForm, exclude=[], extra=1, can_delete=False,
)

SuperadminFormSet = inlineformset_factory(
    User, models.Superadmin, form=SuperadminForm, exclude=[], extra=1, can_delete=False,
)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["score", "text"]
        labels = {
            "score": _("Score"),
            "text": _("Text"),
        }
