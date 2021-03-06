# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-15 15:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MicroCourse', '0022_auto_20181111_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=64)),
                ('src', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='UnitCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MicroCourse.CourseInfo')),
            ],
        ),
        migrations.AlterField(
            model_name='answer',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 15, 23, 24, 53, 523194)),
        ),
        migrations.AlterField(
            model_name='question',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 15, 23, 24, 53, 522633)),
        ),
        migrations.AddField(
            model_name='files',
            name='unitCourse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MicroCourse.UnitCourse'),
        ),
    ]
