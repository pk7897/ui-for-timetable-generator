# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-21 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0006_auto_20170620_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='WHPD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subid', models.IntegerField(default=0)),
                ('whpd1', models.IntegerField(default=0)),
                ('whpd2', models.IntegerField(default=0)),
                ('whpd3', models.IntegerField(default=0)),
                ('whpd4', models.IntegerField(default=0)),
                ('whpd5', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='subjects',
            name='subtype',
            field=models.CharField(default='Normal', max_length=20),
        ),
        migrations.AddField(
            model_name='subjects',
            name='constr1list',
            field=models.ManyToManyField(to='timetable.WHPD'),
        ),
    ]
