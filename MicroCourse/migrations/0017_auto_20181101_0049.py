# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-31 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MicroCourse', '0016_test_testhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='endDate',
        ),
        migrations.RemoveField(
            model_name='test',
            name='name',
        ),
        migrations.RemoveField(
            model_name='test',
            name='startDate',
        ),
        migrations.AddField(
            model_name='test',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]