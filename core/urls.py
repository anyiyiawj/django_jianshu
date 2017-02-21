from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',index,name='index'),#必须写成这个样子，没有^匹配所有
    url(r'^logout/$',user_logout,name='logout'),
    url(r'^topics/$',topics,name='topics'),
    url(r'^people/(?P<user_id>\d+)/$',profile,name='profile'),
    url(r'follow/(?P<user_id>\d+)/$',follow,name='follow'),
    url(r'unfollow/(?P<user_id>\d+)/$',unfollow,name='unfollow'),
    url(r'follower/>(?P<user_id>\d+)/$',follower,name='follower'),
    url(r'following/>(?P<user_id>\d+)/$',following,name='following'),
]