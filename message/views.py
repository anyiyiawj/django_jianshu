from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Message

@login_required
def inbox(request):#收信箱，展示第一个
    conversations = Message.get_conversations(user=request.user)#当前用户的对话信息列表（收信者，日期，未读条数）
    active_conversation = None
    messages = None
    if conversations:
        conversation = conversations[0]  #活动的消息，即第一个消息者
        active_conversation = conversation['user'].username  #活动对话的发信者名字
        messages = Message.objects.filter(user=request.user,conversation=conversation['user']) #活动的对话类
        messages.update(is_read=True) #更新
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0 #未读条数更改
    return render(request, 'message/inbox.html', {'user':request.user,'messages': messages,'conversations': conversations,'active': active_conversation})


@login_required
def messages(request, userid):#某个人消息
    conversations = Message.get_conversations(user=request.user)
    active_conversation = User.objects.get(id=userid)
    messages = Message.objects.filter(user=request.user,conversation__username=active_conversation)
    messages.update(is_read=True)
    for conversation in conversations:
        if conversation['user'].username == active_conversation:
            conversation['unread'] = 0
    print(request.user)
    return render(request, 'message/inbox.html',{'messages': messages,'conversations': conversations,'active': active_conversation,'user':request.user})


@login_required
def new(request):#发送消息
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')#收信人
        try:
            to_user = User.objects.get(username=to_user_username)
            id=to_user.id
        except Exception:
            try:
                to_user_username = to_user_username[to_user_username.rfind('(')+1:len(to_user_username)-1]
                to_user = User.objects.get(username=to_user_username)
                id = to_user.id
            except Exception:
                return redirect('/message/new/')
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return redirect('/message/new/')
        if from_user != to_user:
            Message.send_message(from_user, to_user, message)#发送消息
        return redirect('/message/{0}/'.format(id))
    else:
        conversations = Message.get_conversations(user=request.user)
        return render(request, 'message/new.html',{'user':request.user,'conversations': conversations})
