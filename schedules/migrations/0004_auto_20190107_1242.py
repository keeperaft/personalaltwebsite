# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-07 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_schoolsection_is_special_needs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='teacher_name',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
