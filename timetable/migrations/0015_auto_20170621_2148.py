# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-21 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0014_auto_20170621_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='slot_check',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='constr1list',
            field=models.ManyToManyField(to='timetable.Whpd'),
        ),
    ]
