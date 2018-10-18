# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from .models import CityDict, CourseOrg, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from django.db.models import Q
from operation.models import UserFavorite
import json
from courses.models import Course
# Create your views here.


class OrgView(View):
    def get(self, request):
        all_org = CourseOrg.objects.all()
        cities = CityDict.objects.all()

        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_org = all_org.filter(Q(name__icontains=search_keywords)|
                                     Q(desc__icontains=search_keywords))

        hot_orgs = all_org.order_by("-click_nums")[:5]

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_org = all_org.order_by("-students")
            elif sort == "course_nums":
                all_org = all_org.order_by("-course_nums")

        # classification
        city_id = request.GET.get("city", "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        category = request.GET.get("ct", "")
        if category:
            all_org = all_org.filter(category=category)

        org_num = all_org.count()
        # pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org, 5, request=request)

        org = p.page(page)

        return render(request, 'org-list.html', {"all_org": org,
                                                 "cities": cities,
                                                 "org_num": org_num,
                                                 "city_id": city_id,
                                                 "category": category,
                                                 "hot_orgs": hot_orgs,
                                                 "sort": sort,
                                                 })


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            suc_dict = {'status': 'success'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")
        else:
            error_dict = {'status': 'fail', 'msg': u'填写错误'}
            return HttpResponse(json.dumps(error_dict), content_type="application/json")


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        current_page = "course"
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = "desc"
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        current_page = "teahcer"
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teachers': all_teachers,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            fail_dict = {'status': 'fail', 'msg': '用户未登录'}
            return HttpResponse(json.dumps(fail_dict), content_type="application/json")
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_num -= 1
                if course.fav_num<0:
                    course.fav_num=0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums<0:
                    course_org.fav_nums=0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums<0:
                    teacher.fav_nums=0
                teacher.save()
            suc_dict = {'status': 'success', 'msg': '收藏'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")

        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_num += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                suc_dict = {'status': 'success', 'msg': '已收藏'}
                return HttpResponse(json.dumps(suc_dict), content_type="application/json")

            else:
                fail_dict = {'status': 'fail', 'msg': '收藏出错'}
                return HttpResponse(json.dumps(fail_dict), content_type="application/json")


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords))

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")
        teacher_count = all_teachers.count()
        # pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "hot_teachers": hot_teachers,
            "sort": sort,
            "teacher_count": teacher_count,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        courses = Course.objects.filter(teacher=teacher)
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "courses": courses,
            "hot_teachers": hot_teachers,
            "has_fav_teacher": has_fav_teacher,
            "has_fav_org": has_fav_org,

        })
