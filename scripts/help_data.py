#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# ./manage.py dumpscript courses profiles account.EmailAddress
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction


class BasicImportHelper(object):
    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(
        self,
        original_class,
        original_pk_name,
        the_class,
        pk_name,
        pk_value,
        obj_content,
    ):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = {pk_name: pk_value}
        the_obj = the_class.objects.get(**search_data)
        # print(the_obj)
        return the_obj

    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper

    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type(
        "DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper), {}
    )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if "import_helper" in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
    from dateutil.tz import tzoffset
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)


def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()


def import_data():
    # Initial Imports
    from django.contrib.auth.models import Group

    # Processing model: opencourse.courses.models.City

    from opencourse.courses.models import City

    courses_city_1 = City()
    courses_city_1.codepostal = None
    courses_city_1.name = "London"
    courses_city_1.name_en = "London"
    courses_city_1.name_fr = "Londres"
    courses_city_1.latitude_south = None
    courses_city_1.latitude_north = None
    courses_city_1.longitude_west = None
    courses_city_1.longitude_east = None
    courses_city_1.latitude_southa = None
    courses_city_1.latitude_northa = None
    courses_city_1.longitude_westa = None
    courses_city_1.longitude_easta = None
    courses_city_1.category_1 = None
    courses_city_1.category_2 = None
    courses_city_1 = importer.save_or_locate(courses_city_1)

    courses_city_2 = City()
    courses_city_2.codepostal = None
    courses_city_2.name = "Paris"
    courses_city_2.name_en = "Paris"
    courses_city_2.name_fr = "Paris"
    courses_city_2.latitude_south = None
    courses_city_2.latitude_north = None
    courses_city_2.longitude_west = None
    courses_city_2.longitude_east = None
    courses_city_2.latitude_southa = None
    courses_city_2.latitude_northa = None
    courses_city_2.longitude_westa = None
    courses_city_2.longitude_easta = None
    courses_city_2.category_1 = None
    courses_city_2.category_2 = None
    courses_city_2 = importer.save_or_locate(courses_city_2)

    courses_city_3 = City()
    courses_city_3.codepostal = None
    courses_city_3.name = "Washington"
    courses_city_3.name_en = "Washington"
    courses_city_3.name_fr = "Washington"
    courses_city_3.latitude_south = None
    courses_city_3.latitude_north = None
    courses_city_3.longitude_west = None
    courses_city_3.longitude_east = None
    courses_city_3.latitude_southa = None
    courses_city_3.latitude_northa = None
    courses_city_3.longitude_westa = None
    courses_city_3.longitude_easta = None
    courses_city_3.category_1 = None
    courses_city_3.category_2 = None
    courses_city_3 = importer.save_or_locate(courses_city_3)

    courses_city_4 = City()
    courses_city_4.codepostal = None
    courses_city_4.name = "Berlin"
    courses_city_4.name_en = "Berlin"
    courses_city_4.name_fr = "Berlin"
    courses_city_4.latitude_south = None
    courses_city_4.latitude_north = None
    courses_city_4.longitude_west = None
    courses_city_4.longitude_east = None
    courses_city_4.latitude_southa = None
    courses_city_4.latitude_northa = None
    courses_city_4.longitude_westa = None
    courses_city_4.longitude_easta = None
    courses_city_4.category_1 = None
    courses_city_4.category_2 = None
    courses_city_4 = importer.save_or_locate(courses_city_4)

    courses_city_5 = City()
    courses_city_5.codepostal = None
    courses_city_5.name = "Stockholm"
    courses_city_5.name_en = "Stockholm"
    courses_city_5.name_fr = "Stockholm"
    courses_city_5.latitude_south = None
    courses_city_5.latitude_north = None
    courses_city_5.longitude_west = None
    courses_city_5.longitude_east = None
    courses_city_5.latitude_southa = None
    courses_city_5.latitude_northa = None
    courses_city_5.longitude_westa = None
    courses_city_5.longitude_easta = None
    courses_city_5.category_1 = None
    courses_city_5.category_2 = None
    courses_city_5 = importer.save_or_locate(courses_city_5)

    # Processing model: opencourse.courses.models.CourseLevel

    from opencourse.courses.models import CourseLevel

    courses_courselevel_1 = CourseLevel()
    courses_courselevel_1.name = "Beginner"
    courses_courselevel_1.name_en = "Beginner"
    courses_courselevel_1.name_fr = "Débutant"
    courses_courselevel_1.description = None
    courses_courselevel_1 = importer.save_or_locate(courses_courselevel_1)

    courses_courselevel_2 = CourseLevel()
    courses_courselevel_2.name = "Intermediate"
    courses_courselevel_2.name_en = "Intermediate"
    courses_courselevel_2.name_fr = "Moyen"
    courses_courselevel_2.description = None
    courses_courselevel_2 = importer.save_or_locate(courses_courselevel_2)

    courses_courselevel_3 = CourseLevel()
    courses_courselevel_3.name = "Advanced"
    courses_courselevel_3.name_en = "Advanced"
    courses_courselevel_3.name_fr = "Avancé"
    courses_courselevel_3.description = None
    courses_courselevel_3 = importer.save_or_locate(courses_courselevel_3)

    # Processing model: opencourse.courses.models.CourseDuration

    from opencourse.courses.models import CourseDuration

    courses_courseduration_1 = CourseDuration()
    courses_courseduration_1.duration = 30
    courses_courseduration_1 = importer.save_or_locate(courses_courseduration_1)

    courses_courseduration_2 = CourseDuration()
    courses_courseduration_2.duration = 45
    courses_courseduration_2 = importer.save_or_locate(courses_courseduration_2)

    courses_courseduration_3 = CourseDuration()
    courses_courseduration_3.duration = 60
    courses_courseduration_3 = importer.save_or_locate(courses_courseduration_3)

    courses_courseduration_4 = CourseDuration()
    courses_courseduration_4.duration = 90
    courses_courseduration_4 = importer.save_or_locate(courses_courseduration_4)

    courses_courseduration_5 = CourseDuration()
    courses_courseduration_5.duration = 120
    courses_courseduration_5 = importer.save_or_locate(courses_courseduration_5)

    # Processing model: opencourse.courses.models.CourseAge

    from opencourse.courses.models import CourseAge

    courses_courseage_1 = CourseAge()
    courses_courseage_1.max = None
    courses_courseage_1.name = "Infants (0-3 years old)"
    courses_courseage_1.name_en = "Infants (0-3 years old)"
    courses_courseage_1.name_fr = "Nourrissons (0-3 ans)"
    courses_courseage_1 = importer.save_or_locate(courses_courseage_1)

    courses_courseage_2 = CourseAge()
    courses_courseage_2.max = None
    courses_courseage_2.name = "Preschool children (4-6 years old)"
    courses_courseage_2.name_en = "Preschool children (4-6 years old)"
    courses_courseage_2.name_fr = "Enfants d'âge préscolaire (4-6 ans)"
    courses_courseage_2 = importer.save_or_locate(courses_courseage_2)

    courses_courseage_3 = CourseAge()
    courses_courseage_3.max = None
    courses_courseage_3.name = "Children (7-12 years old)"
    courses_courseage_3.name_en = "Children (7-12 years old)"
    courses_courseage_3.name_fr = "Enfants (7-12 ans)"
    courses_courseage_3 = importer.save_or_locate(courses_courseage_3)

    courses_courseage_4 = CourseAge()
    courses_courseage_4.max = None
    courses_courseage_4.name = "Teenagers (13-17 years old)"
    courses_courseage_4.name_en = "Teenagers (13-17 years old)"
    courses_courseage_4.name_fr = "Adolescents (13-17 ans)"
    courses_courseage_4 = importer.save_or_locate(courses_courseage_4)

    courses_courseage_5 = CourseAge()
    courses_courseage_5.max = None
    courses_courseage_5.name = "Adults (18-64 years old)"
    courses_courseage_5.name_en = "Adults (18-64 years old)"
    courses_courseage_5.name_fr = "Adultes (18-64 ans)"
    courses_courseage_5 = importer.save_or_locate(courses_courseage_5)

    courses_courseage_6 = CourseAge()
    courses_courseage_6.max = None
    courses_courseage_6.name = "Seniors (65+ years old)"
    courses_courseage_6.name_en = "Seniors (65+ years old)"
    courses_courseage_6.name_fr = "Aînés (65 ans)"
    courses_courseage_6 = importer.save_or_locate(courses_courseage_6)

    # Processing model: opencourse.courses.models.CourseArea

    from opencourse.courses.models import CourseArea

    courses_coursearea_1 = CourseArea()
    courses_coursearea_1.name = "Math"
    courses_coursearea_1.name_en = "Math"
    courses_coursearea_1.name_fr = "Math"
    courses_coursearea_1.description = None
    courses_coursearea_1 = importer.save_or_locate(courses_coursearea_1)

    courses_coursearea_2 = CourseArea()
    courses_coursearea_2.name = "Physics"
    courses_coursearea_2.name_en = "Physics"
    courses_coursearea_2.name_fr = "La physique"
    courses_coursearea_2.description = None
    courses_coursearea_2 = importer.save_or_locate(courses_coursearea_2)

    courses_coursearea_3 = CourseArea()
    courses_coursearea_3.name = "Chemistry"
    courses_coursearea_3.name_en = "Chemistry"
    courses_coursearea_3.name_fr = "Chimie"
    courses_coursearea_3.description = None
    courses_coursearea_3 = importer.save_or_locate(courses_coursearea_3)

    courses_coursearea_4 = CourseArea()
    courses_coursearea_4.name = "Biology"
    courses_coursearea_4.name_en = "Biology"
    courses_coursearea_4.name_fr = "La biologie"
    courses_coursearea_4.description = None
    courses_coursearea_4 = importer.save_or_locate(courses_coursearea_4)

    # Processing model: opencourse.courses.models.CourseLanguage

    from opencourse.courses.models import CourseLanguage

    courses_courselanguage_1 = CourseLanguage()
    courses_courselanguage_1.name = "English"
    courses_courselanguage_1.name_en = "English"
    courses_courselanguage_1.name_fr = "Anglais"
    courses_courselanguage_1.tag = None
    courses_courselanguage_1 = importer.save_or_locate(courses_courselanguage_1)

    courses_courselanguage_2 = CourseLanguage()
    courses_courselanguage_2.name = "French"
    courses_courselanguage_2.name_en = "French"
    courses_courselanguage_2.name_fr = "Le français"
    courses_courselanguage_2.tag = None
    courses_courselanguage_2 = importer.save_or_locate(courses_courselanguage_2)

    courses_courselanguage_3 = CourseLanguage()
    courses_courselanguage_3.name = "Arabic"
    courses_courselanguage_3.name_en = "Arabic"
    courses_courselanguage_3.name_fr = "Arabe"
    courses_courselanguage_3.tag = None
    courses_courselanguage_3 = importer.save_or_locate(courses_courselanguage_3)

    courses_courselanguage_4 = CourseLanguage()
    courses_courselanguage_4.name = "Spanish"
    courses_courselanguage_4.name_en = "Spanish"
    courses_courselanguage_4.name_fr = "Espagnol"
    courses_courselanguage_4.tag = None
    courses_courselanguage_4 = importer.save_or_locate(courses_courselanguage_4)

    courses_courselanguage_5 = CourseLanguage()
    courses_courselanguage_5.name = "Chinese"
    courses_courselanguage_5.name_en = "Chinese"
    courses_courselanguage_5.name_fr = "Japonais"
    courses_courselanguage_5.tag = None
    courses_courselanguage_5 = importer.save_or_locate(courses_courselanguage_5)

    courses_courselanguage_6 = CourseLanguage()
    courses_courselanguage_6.name = "Hindi"
    courses_courselanguage_6.name_en = "Hindi"
    courses_courselanguage_6.name_fr = "Hindi"
    courses_courselanguage_6.tag = None
    courses_courselanguage_6 = importer.save_or_locate(courses_courselanguage_6)

    courses_courselanguage_7 = CourseLanguage()
    courses_courselanguage_7.name = "Russian"
    courses_courselanguage_7.name_en = "Russian"
    courses_courselanguage_7.name_fr = "Russe"
    courses_courselanguage_7.tag = None
    courses_courselanguage_7 = importer.save_or_locate(courses_courselanguage_7)

    # Processing model: opencourse.courses.models.CourseLocationType

    from opencourse.courses.models import CourseLocationType

    courses_courselocationtype_1 = CourseLocationType()
    courses_courselocationtype_1.name = "Teacher's"
    courses_courselocationtype_1.name_en = "Teacher's"
    courses_courselocationtype_1.name_fr = "Chez l'enseignant"
    courses_courselocationtype_1 = importer.save_or_locate(courses_courselocationtype_1)

    courses_courselocationtype_2 = CourseLocationType()
    courses_courselocationtype_2.name = "Students's"
    courses_courselocationtype_2.name_en = "Students's"
    courses_courselocationtype_2.name_fr = "Étudiant"
    courses_courselocationtype_2 = importer.save_or_locate(courses_courselocationtype_2)

    courses_courselocationtype_3 = CourseLocationType()
    courses_courselocationtype_3.name = "Via webcam"
    courses_courselocationtype_3.name_en = "Via webcam"
    courses_courselocationtype_3.name_fr = "Par webcam"
    courses_courselocationtype_3 = importer.save_or_locate(courses_courselocationtype_3)

    # Processing model: opencourse.courses.models.Currency

    from opencourse.courses.models import Currency

    courses_currency_1 = Currency()
    courses_currency_1.name = "Moroccan dirham"
    courses_currency_1.iso_code = "MAD"
    courses_currency_1.symbol = ".د.م"
    courses_currency_1 = importer.save_or_locate(courses_currency_1)

    courses_currency_2 = Currency()
    courses_currency_2.name = "US dollar"
    courses_currency_2.iso_code = "USD"
    courses_currency_2.symbol = "$"
    courses_currency_2 = importer.save_or_locate(courses_currency_2)

    courses_currency_3 = Currency()
    courses_currency_3.name = "Euro"
    courses_currency_3.iso_code = "EUR"
    courses_currency_3.symbol = "€"
    courses_currency_3 = importer.save_or_locate(courses_currency_3)

    # Processing model: opencourse.courses.models.HandoutSection

    from opencourse.courses.models import HandoutSection

    courses_handoutsection_1 = HandoutSection()
    courses_handoutsection_1.name = "Lectures"
    courses_handoutsection_1 = importer.save_or_locate(courses_handoutsection_1)

    courses_handoutsection_2 = HandoutSection()
    courses_handoutsection_2.name = "Practice"
    courses_handoutsection_2 = importer.save_or_locate(courses_handoutsection_2)

    courses_handoutsection_3 = HandoutSection()
    courses_handoutsection_3.name = "Exams"
    courses_handoutsection_3 = importer.save_or_locate(courses_handoutsection_3)
