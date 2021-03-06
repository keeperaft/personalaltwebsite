# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-31 04:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_auto_20190106_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='lessonplan',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.Topic'),
        ),
    ]
