# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-06 04:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_auto_20180911_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolsection',
            name='is_special_needs',
            field=models.BooleanField(default=False),
        ),
    ]