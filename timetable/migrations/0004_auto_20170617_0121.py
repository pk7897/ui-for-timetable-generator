# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-17 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_auto_20170617_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facname', models.CharField(max_length=120)),
                ('hours', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subname', models.CharField(max_length=100)),
                ('faclist', models.ManyToManyField(null=True, to='timetable.Faculty')),
            ],
        ),
        migrations.AddField(
            model_name='classes',
            name='subj_list',
            field=models.ManyToManyField(null=True, to='timetable.Subjects'),
        ),
        migrations.AddField(
            model_name='groups',
            name='sublist',
            field=models.ManyToManyField(null=True, to='timetable.Subjects'),
        ),
    ]
