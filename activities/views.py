from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response

from  .models import Notification

@login_required
def notifications(request):#阅读通知
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    unread = Notification.objects.filter(to_user=user, is_read=False)#未读标记为已读
    for notification in unread:
        notification.is_read = True
        notification.save()
    return render_to_response( 'activities/noti.html',{'user':request.user,'notifications': notifications})

@login_required
def last_notifications(request):#未读的消息
    user = request.user
    notifications = Notification.objects.filter(to_user=user,is_read=False)[:5]#最近5条未读
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return render_to_response('activities/noti_last.html',{'notifications': notifications})

@login_required
def check_notifications(request):#未读消息的数目
    user = request.user
    notifications = Notification.objects.filter(to_user=user,is_read=False)[:5]
    return HttpResponse(len(notifications))


