# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-28 00:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20180727_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='\u89c6\u9891\u5730\u5740'),
        ),
    ]
