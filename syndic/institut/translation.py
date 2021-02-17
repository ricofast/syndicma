from modeltranslation.translator import register, TranslationOptions
from . import models


@register(models.Academicyear)
class AcademicyearTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.City)
class CityTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.Holidays)
class HolidaysTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.Coursearea)
class AreaTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.CourseLanguage)
class LanguageTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.Schoolgroup)
class SchoolgroupTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.HandoutSection)
class SectionTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.Center)
class CenterTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.Centerlevel)
class CenterLevelTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.Grade)
class GradeTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.Classe)
class ClasseTranslationOptions(TranslationOptions):
    fields = ["name"]

