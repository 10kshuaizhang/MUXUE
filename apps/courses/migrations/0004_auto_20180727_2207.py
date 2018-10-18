# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-27 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=20, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(max_length=20, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
    ]
