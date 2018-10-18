# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
import json
from django.db.models import Q
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]

        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                                    Q(desc__icontains=search_keywords))

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")
        # pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "hot_courses": hot_courses,
            "sort": sort
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
        else:
            related_courses = []

        return render(request, "course-detail.html", {
            "course": course,
            "related_courses": related_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        all_resources = CourseResource.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            user_courses.UserCourse.objects.filter(user=request.user, course=course)
            user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "related_courses": related_courses,
        })


class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        usercourses = UserCourse.objects.filter(course=course)
        user_ids = [courses.user.id for courses in usercourses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "related_courses": related_courses,
            "video": video,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        usercourses = UserCourse.objects.filter(course=course)
        user_ids = [courses.user.id for courses in usercourses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "related_courses": related_courses,
        })


class AddCommentsView(View):

    def post(self, request):

        if not request.user.is_authenticated():
            fail_dict = {'status': 'fail', 'msg': '用户未登录'}
            return HttpResponse(json.dumps(fail_dict), content_type="application/json")

        comments = request.POST.get("comments", "")
        course_id = request.POST.get("course_id", 0)

        if comments and course_id != 0:
            coursecomment = CourseComments()
            coursecomment.course = Course.objects.get(id=int(course_id))
            coursecomment.user = request.user
            coursecomment.comments = comments
            coursecomment.save()
            suc_dict = {'status': 'success', 'msg': '评论成功！'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")

        else:
            fail_dict = {'status': 'fail', 'msg': '评论出错！'}
            return HttpResponse(json.dumps(fail_dict), content_type="application/json")




