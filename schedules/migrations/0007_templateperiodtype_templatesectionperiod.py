# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-11-21 04:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolyears', '0005_auto_20190327_2316'),
        ('schedules', '0006_sectionperiod_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplatePeriodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.SmallIntegerField()),
                ('school', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='schoolyears.School')),
                ('school_period_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.SchoolPeriodType')),
            ],
        ),
        migrations.CreateModel(
            name='TemplateSectionPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.SmallIntegerField(default=0)),
                ('school_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.SchoolPeriod')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.Section')),
            ],
        ),
    ]
