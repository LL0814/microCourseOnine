# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-23 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MicroCourse', '0012_taskinfo_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskinfo',
            old_name='standardAnwsers',
            new_name='standardAnswers',
        ),
    ]