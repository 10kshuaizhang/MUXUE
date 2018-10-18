"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView
import xadmin
from users.views import LoginView, RegisterView, ActiveView, ForgetPwdView, ResetPwdView, ModifyPwdView
from users.views import LogoutView, IndexView
from .settings import MEDIA_ROOT#, STATIC_ROOT
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^course/', include('courses.urls', namespace='course')),
    url(r'^users/', include('users.urls', namespace='users')),
    #url(r'static/(?P<path>.*)/$', serve, {"document_root": STATIC_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

handler403 = 'users.views.page_forbbiden'
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.server_error'
