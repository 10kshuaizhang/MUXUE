# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-03 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180716_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '\u6ce8\u518c'), ('forget', '\u627e\u56de'), ('update_email', '\u4fee\u6539\u90ae\u7bb1')], max_length=10, verbose_name='\u53d1\u9001\u7c7b\u578b'),
        ),
    ]
