import xadmin
from .models import Course, CourseResource, Video, Lesson, BannerCourse


class CourseAdmin(object):

    list_display = ['name','desc','detail','learn_time','add_time','degree','students','fav_num','click_num','image']
    search_field = ['name','desc','detail','learn_time','degree','students','fav_num','click_num','image']
    list_filter = ['name','desc','detail','learn_time','add_time','degree','students','fav_num','click_num','image']
    ordering = ['-click_num']
    readonly_fields = ['click_num']
    exclude = ['fav_num']
    list_editable = ['desc']
    #refresh_times = [10]
    style_fields = {"detail": "ueditor"}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class BannerCourseAdmin(object):

    list_display = ['name','desc','detail','learn_time','add_time','degree','students','fav_num','click_num','image']
    search_field = ['name','desc','detail','learn_time','degree','students','fav_num','click_num','image']
    list_filter = ['name','desc','detail','learn_time','add_time','degree','students','fav_num','click_num','image']
    ordering = ['-click_num']
    readonly_fields = ['click_num']
    exclude = ['fav_num']

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'add_time','download']
    search_field = ['course', 'name','download']
    list_filter = ['course', 'name','add_time','download']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_field = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_field = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
