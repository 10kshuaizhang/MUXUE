import xadmin
from .models import CourseComments, UserAsk, UserCourse, UserFavorite, UserMessage


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_type', 'fav_id', 'add_time']
    list_filter = ['user', 'fav_type', 'fav_id', 'add_time']
    search_fields = ['user', 'fav_type', 'fav_id']


class UserMessageAdmin(object):
    list_display = ['user', 'has_read', 'message', 'add_time']
    list_filter = ['user', 'has_read', 'message', 'add_time']
    search_fields = ['user', 'has_read', 'message', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)