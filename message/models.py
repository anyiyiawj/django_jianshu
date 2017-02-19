from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max


class Message(models.Model):    #消息
    user = models.ForeignKey(User, related_name='+')    #发信人
    message = models.TextField(max_length=1000, blank=True) #信息内容
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+')  #收信人
    from_user = models.ForeignKey(User, related_name='+')  #发信人
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.message

    @staticmethod
    def send_message(from_user, to_user, message):#创建
        message = message[:1000]
        current_user_message = Message(from_user=from_user,message=message,user=from_user,conversation=to_user,is_read=True)#创建我发的东西，我来看
        current_user_message.save()
        Message(from_user=from_user,conversation=from_user,message=message,user=to_user).save()#创建我发的东西，别人来看
        return current_user_message

    @staticmethod
    def get_conversations(user):  #返回一个字典组成的列表，有收信人，有日期，有是否读过的条数
        conversations = Message.objects.filter(user=user).values('conversation').annotate(last=Max('date')).order_by('-last')#返回一个按时间排序过的ValueQueryset,（收信人id和last属性）
        users = []
        for conversation in conversations:
            users.append({
                'user': User.objects.get(pk=conversation['conversation']),#对话方
                'last': conversation['last'],#对话的最晚时间
                'unread': Message.objects.filter(user=user,conversation__pk=conversation[ 'conversation'],is_read=False).count(),#未读条数
                })
        return users