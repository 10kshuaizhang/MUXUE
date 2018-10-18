from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, MyCourseView, SendEmailCodeView
from .views import UpdateMailView, MyFavOrgView, MyFavCourseView, MyFavTeacherView, MyMessageView


urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),

    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="pwd_reset"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="my_course"),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    url(r'^update_email/$', UpdateMailView.as_view(), name="updatemail"),
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),

]
