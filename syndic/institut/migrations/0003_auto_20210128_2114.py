# Generated by Django 3.0.5 on 2021-01-28 21:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institut', '0002_auto_20210128_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentnotification',
            name='notifydate',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 28, 21, 14, 35, 495923)),
        ),
    ]