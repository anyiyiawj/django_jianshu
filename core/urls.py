from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',index,name='index'),#必须写成这个样子，没有^匹配所有
    url(r'^logout/$',user_logout,name='logout'),
    url(r'^topics/$',topics,name='topics'),
    url(r'^people/(?P<user_id>\d+)/$',profile,name='profile'),
]