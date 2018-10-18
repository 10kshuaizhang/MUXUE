# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-12 16:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u8bfe\u7a0b\u540d')),
                ('desc', models.CharField(max_length=200, verbose_name='\u8bfe\u7a0b\u63cf\u8ff0')),
                ('detail', models.TextField(verbose_name='\u7ec6\u8282')),
                ('learn_time', models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u65f6\u957f')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, max_length=20, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('degree', models.CharField(choices=[('cj', '\u521d\u7ea7'), ('zj', '\u4e2d\u7ea7'), ('gj', '\u9ad8\u7ea7')], max_length=5, verbose_name='\u96be\u5ea6')),
                ('students', models.CharField(max_length=100, verbose_name='\u5b66\u751f\u4eba\u6570')),
                ('fav_num', models.IntegerField(default=0, verbose_name='\u6536\u85cf\u6570')),
                ('click_num', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6570')),
                ('image', models.ImageField(max_length=200, upload_to='courses/%Y/%m', verbose_name='\u5c01\u9762\u56fe')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b',
                'verbose_name_plural': '\u8bfe\u7a0b',
            },
        ),
        migrations.CreateModel(
            name='CourseResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u8bfe\u7a0b\u8d44\u6e90')),
                ('download', models.FileField(upload_to='course/resouce/%Y%m', verbose_name='\u4e0b\u8f7d\u5730\u5740')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, max_length=20, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u8d44\u6e90',
                'verbose_name_plural': '\u8bfe\u7a0b\u8d44\u6e90',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u7ae0\u8282\u540d')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, max_length=20, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='\u6240\u5c5e\u8bfe\u7a0b')),
            ],
            options={
                'verbose_name': '\u7ae0\u8282',
                'verbose_name_plural': '\u7ae0\u8282',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u89c6\u9891\u540d')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, max_length=20, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson', verbose_name='\u6240\u5c5e\u7ae0\u8282')),
            ],
            options={
                'verbose_name': '\u7ae0\u8282\u89c6\u9891',
                'verbose_name_plural': '\u7ae0\u8282\u89c6\u9891',
            },
        ),
    ]
