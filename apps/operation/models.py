# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

from users.models import UserProfile
from courses.models import Course


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机")
    course_name = models.CharField(max_length=50, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"用户评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    fav_type = models.IntegerField(choices=((1, u"课程"), (2, u"课程机构"), (3, u"讲师")))
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接收用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    message = models.CharField(max_length=200, verbose_name=u"消息")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.message


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"姓名")
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name
