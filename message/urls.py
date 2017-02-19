from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', inbox, name='inbox'),#收信箱
    url(r'^new/$',new,name='new_message'),#发送邮件
    url(r'^(?P<userid>\d+)/$', messages, name='messages'),#个人消息
]
