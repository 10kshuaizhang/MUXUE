# -*- coding:utf-8 -*-
from django import forms
from operation.models import UserAsk
import re


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        reg = r"1\d{10}"
        p = re.compile(reg)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile invalid")



