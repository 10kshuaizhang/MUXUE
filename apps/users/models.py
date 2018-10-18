# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")))
    address = models.CharField(max_length=200, verbose_name=u"地址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"手机")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", verbose_name="头像", max_length=100 )

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def unread_msg(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_time = models.DateField(default=datetime.now, verbose_name="发送时间")
    send_type = models.CharField(verbose_name="发送类型", choices=(("register", u"注册"),
                                                                    ("forget", u"找回"),
                                                                    ("update_email", u"修改")), max_length=30)

    class Meta:
        verbose_name = u"验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="轮播图", max_length=200)
    url = models.URLField(max_length=500, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
