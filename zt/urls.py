"""zt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from core import views as core_views
from activities import views as acti_views
from .settings import *



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',include('core.urls')),
    url(r'^article/',include('article.urls')),
    url(r'^setting/$',core_views.setting,name='setting'),
    url(r'^setting/password/$',core_views.password,name='setpw'),
    url(r'^setting/picture/$',core_views.upload_pic,name='setpic'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),#头像设置
    url(r'^settings/upload_picture/$', core_views.upload_picture,name='upload_picture'),#上传头像
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,name='save_uploaded_picture'),#保存头像
    url(r'^notifications/$', acti_views.notifications,name='notifications'),
    url(r'^notifications/last/$',acti_views.last_notifications,name='last_notification'),
    url(r'^notifications/check/$',acti_views.check_notifications,name='check_notifications'),
    url(r'^message/', include('message.urls')),
    url(r'^media/(?P<path>.*)',serve, {'document_root':MEDIA_ROOT}),
]
