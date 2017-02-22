from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^add/$',add,name='add'),
    url(r'^(?P<article_id>\d+)/$',article,name='article'),
    url(r'^notes/(?P<notes_id>\d+)/$',notes,name='notes'),
    url(r'^topic/(?P<topic_id>\d+)/$',topic,name='topic'),
    url(r'^(?P<article_id>\d+)/edit/$',edit,name='edit'),
    url(r'^draft/$',draft,name='draft'),
    url(r'^(?P<article_id>\d+)/comment$',comment,name='comment'),
    url(r'comment/(?P<comment_id>\d+)/$',dele_com,name='dele_com'),
    url(r'^(?P<article_id>\d+)/delete$',art_delete,name='art_delete'),
    url(r'^notes/(?P<notes_id>\d+)/delete$',notes_delete,name='notes_delete'),
    url(r'^like/$',like,name='like'),
]