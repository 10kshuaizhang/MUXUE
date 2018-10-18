# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.hashers import make_password
import json
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
# Create your views here.

from users.models import UserProfile, EmailVerifyRecord, Banner
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from users.forms import UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import Teacher
from courses.models import CourseOrg, Course


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": " Not Active"})
            else:
                return render(request, "login.html", {"msg": "error!", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            if UserProfile.objects.get(email=email):
                return render(request, "register.html", {"register_form": register_form, "msg": u"用户已存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.email = email
            user_profile.username = email
            user_profile.password = make_password(pass_word)
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎欢迎热烈欢迎！"
            user_message.save()

            send_register_email(email, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetPwdView(View):
    """
    reset password
    """
    def get(self, request, reset_code):
        all_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg":u"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            suc_dict = {'status': "success", "msg": u"邮箱修改成功"}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")

        else:
            return HttpResponse(json.dumps(user_form.errors), content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()

            suc_dict = {'status': 'success'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")
        else:
            error_dict = {'status': 'fail', 'msg': u'错误'}
            return HttpResponse(json.dumps(error_dict), content_type="application/json")


class UpdatePwdView(LoginRequiredMixin, View):
    """
    modify password in usercenter( logined)
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            suc_dic = {'status': "success"}
            fail_dic = {'status': "fail", "msg": u"密码不一致"}
            if pwd1 != pwd2:
                return HttpResponse(json.dumps(fail_dic), content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse(json.dumps(suc_dic), content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors))


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "my_courses": my_courses,
        })


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get("email")
        if UserProfile.objects.filter(email=email):
            fail_dic = {"email": u"邮箱已存在"}
            return HttpResponse(json.dumps(fail_dic), content_type="application/json")
        send_register_email(email, "update_email")
        suc_dict = {'status': "success", "msg": u"邮箱修改成功"}
        return HttpResponse(json.dumps(suc_dict), content_type="application/json")


class UpdateMailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code,send_type="update_email")
        if existed_record:
            request.user.email = email
            request.user.save()
            suc_dict = {'status': "success", "msg": u"邮箱修改成功"}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")

        else:
            fail_dic = {"email": u"验证码错误"}
            return HttpResponse(json.dumps(fail_dic), content_type="application/json")


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        orgs = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            orgs.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        orgs = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            orgs.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teachers = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teachers.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        courses = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_courses in fav_courses:
            course_id = fav_courses.fav_id
            course = Course.objects.get(id=course_id)
            courses.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        unread_msgs = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_msg in unread_msgs:
            unread_msg.has_read = True
            unread_msg.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages": messages,
        })


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_forbbiden(request):
    from django.shortcuts import render_to_response
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response


def server_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response