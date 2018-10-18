import xadmin
from .models import CourseOrg, CityDict, Teacher


class CityDicAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):

    list_display = ['name','desc','add_time','click_nums','image','address','city']
    search_fields = ['name','desc','click_nums','image','address','city']
    list_filter = ['name','desc','add_time','click_nums','image','address','city']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):

    list_display = ['org','name','add_time', 'fav_nums', 'click_nums', 'work_company','work_position','work_years']
    search_fields = ['org','name', 'fav_nums', 'click_nums', 'work_company','work_position','work_years']
    list_filter = ['org','name','add_time', 'fav_nums', 'click_nums', 'work_company','work_position','work_years']


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDicAdmin)
xadmin.site.register(Teacher, TeacherAdmin)