# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-23 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20180723_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=models.CharField(max_length=200, verbose_name='\u673a\u6784\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='name',
            field=models.CharField(max_length=20, verbose_name='\u673a\u6784\u540d'),
        ),
    ]
