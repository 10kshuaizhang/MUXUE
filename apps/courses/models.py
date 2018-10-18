# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"课程名")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    desc = models.CharField(verbose_name=u"课程描述", max_length=200)
    detail = UEditorField(verbose_name=u"课程详情",width=600, height=300, imagePath="courese/ueditor/", filePath="courese/ueditor/",default= "")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长")
    add_time = models.DateTimeField(max_length=20, default=datetime.now, verbose_name=u"添加时间")
    degree = models.CharField(max_length=5, choices=(('cj', u"初级"), ('zj', u"中级"),('gj', u"高级")), verbose_name=u"难度")
    students = models.IntegerField(verbose_name=u"学生人数")
    fav_num = models.IntegerField(default=0, verbose_name=u"收藏数")
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    image = models.ImageField(upload_to="courses/%Y/%m", max_length=200, verbose_name="封面图")
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", blank=True, null=True)
    category = models.CharField(verbose_name=u"课程类别", max_length=20)
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=20)
    need_know = models.CharField(verbose_name=u"课程须知", default="", max_length=300)
    teacher_tell = models.CharField(verbose_name=u"教师寄语", default="", max_length=300)
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_chapter_num(self):
        return self.lesson_set.all().count()

    def get_participate(self):
        return self.usercourse_set.all()[:5]

    def get_course_lessons(self):
        return self.lesson_set.all()


class BannerCourse(Course):

    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"所属课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(max_length=20, default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"所属章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200, default="", verbose_name=u"视频地址")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长")
    add_time = models.DateTimeField(max_length=20, default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "章节视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=100, verbose_name=u"课程资源")
    download = models.FileField(upload_to="course/resouce/%Y%m", verbose_name=u"下载地址")
    add_time = models.DateTimeField(max_length=20, default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
