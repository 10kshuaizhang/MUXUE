# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-27 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default=1, max_length=200, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
            preserve_default=False,
        ),
    ]