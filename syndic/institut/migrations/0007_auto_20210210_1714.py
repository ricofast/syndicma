# Generated by Django 3.0.5 on 2021-02-10 17:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20210210_1714'),
        ('institut', '0006_auto_20210210_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='classe',
        ),
        migrations.AlterField(
            model_name='notification',
            name='notifydate',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 10, 17, 14, 32, 431685)),
        ),
        migrations.RemoveField(
            model_name='notification',
            name='student',
        ),
        migrations.AddField(
            model_name='notification',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Student'),
        ),
        migrations.AlterField(
            model_name='parentnotification',
            name='notifydate',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 10, 17, 14, 32, 432741)),
        ),
    ]