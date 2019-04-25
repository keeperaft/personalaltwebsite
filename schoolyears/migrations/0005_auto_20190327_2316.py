# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-27 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolyears', '0004_remove_schoolroute_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='school_type',
            field=models.CharField(choices=[('ES', 'Elementary School'), ('JS', 'Junior High School')], default='ES', max_length=32),
        ),
    ]
