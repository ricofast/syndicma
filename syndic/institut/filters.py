from django.utils.translation import ugettext_lazy as _
import django_filters
from . import models
from django_filters import DateFilter
from django import forms


class CourseFilter(django_filters.FilterSet):

    class Meta:
        model = models.Course
        fields = [
            "area",
            "language",

        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        labels = {
            "area": _("Area"),
            "language": _("Language"),
            }
        for filt in self.filters.values():
            filt.label = labels[filt.field_name]


class CenterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Center
        fields = [
            "name",
        ]


class HolidaysFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    startperiod = DateFilter(field_name="startdate", lookup_expr='gte', widget=forms.DateInput(attrs={

                'type': 'date'
            }))
    ednperiod = DateFilter(field_name="startdate", lookup_expr='lte', widget=forms.DateInput(attrs={

                'type': 'date'
            }))
    class Meta:
        model = models.Holidays
        fields = [
            "name",
        ]

