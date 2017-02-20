from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .forms import UserForm,ProfileForm,ChangePasswordForm,ProfilePicForm
from .models import Profile
from article.models import Article
from zt import settings

import os
from PIL import Image

def index(request):#登录页面
    if not request.user.is_authenticated():
        message=""
        if request.method=="POST":
            flag=request.POST.get('flag',None)
            if flag=="登录":
                username=request.POST.get('username',None)
                password=request.POST.get('password',None)
                user=authenticate(username=username,password=password)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return HttpResponseRedirect('/')
                    else:
                        message='你的账号没有被激活'
                else:
                    message="用户名或密码错误"
            elif flag=="注册思苇":
                user_form=UserForm(request.POST)
                pw=request.POST.get('repw',None)
                if user_form.is_valid():
                    cd=user_form.cleaned_data
                    if cd['password']==pw:
                        user=User.objects.create_user(username=cd['username'],password=pw)#这样才能穿
                        print(user.username)
                        user.profile=Profile.objects.get_or_create(user=user)[0]#添加一对一关系
                        user.save()
                        login(request,user)
                        return HttpResponseRedirect('/')
                    else:
                        message='两次密码不一致'
                else:
                    message='你的注册信息填写错误'
            else:
                message='未知错误'
        user_form=UserForm()
        return render_to_response('core/lr.html',{'user_form':user_form,'message':message})
    articles=Article.objects.filter(status='p')
    return render_to_response('core/index.html',{'user':request.user,'articles':articles})#主页面


@login_required
def topics(request):
    articles = request.user.profile.get_article()
    topics =[]

    for article in articles:
        for topic in article.topic.all():
            if topic not in topics:
                topics.append(topic)
    return render_to_response('core/topics.html', {'user':request.user,"topics":topics})  # 主页面

@login_required
def profile(request,user_id):
    viewuser=User.objects.get(id=user_id)    
    return render_to_response('core/profile.html',{'user':request.user,'viewuser':viewuser,'profile':viewuser.profile})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def setting(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data.get('email')
            user.profile.signature = form.cleaned_data.get('signature')
            user.profile.location = form.cleaned_data.get('location')
            print(form.cleaned_data.get('location'))
            user.save()
            user.profile.save()
            return HttpResponseRedirect('/setting/')
    else:
        form = ProfileForm(instance=user, initial={
            'signature': user.profile.signature,
            'location': user.profile.location
            })
    return render_to_response( 'core/settings.html', {'user':request.user,'form': form})

@login_required
def upload_pic(request):
    if request.method=="POST":
        profile_form=ProfilePicForm(request.POST)
        if profile_form.is_valid():
            if 'picture' in request.FILES:
                request.user.profile.picture=request.FILES['picture']
            request.user.profile.save()
    else:
        profile_form=ProfilePicForm()
    return render_to_response('core/picset.html',{'user':request.user,'profile_form':profile_form})


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data.get('old_password')
            print(password)
            user = authenticate(username=user.username, password=password)
            if user:
                new_password = form.cleaned_data.get('new_password')
                print(new_password)
                new_password1 = form.cleaned_data.get('confirm_password')
                print(new_password1)
                if new_password==new_password1:
                    user.set_password(new_password)
                    user.save()
                    login(request,user)
                    return HttpResponseRedirect('/setting/password')
                else:
                    HttpResponseRedirect('/setting/password')#两次密码不一样
            else:
                HttpResponseRedirect('/setting/password')#密码有误

    else:
        form = ChangePasswordForm(instance=user)
    return render_to_response('core/password.html', {'user':request.user,'form': form})


@login_required
def picture(request):
    uploaded_picture = False#是否显示遮罩层
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True
    except Exception:
        pass
    return render_to_response( 'core/picture.html',{'user':request.user,'uploaded_picture':uploaded_picture})

@login_required
def upload_picture(request):#上传图片
    try:
        profile_pictures = settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)#放图片的位置
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'#路径
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)#写入图片
        im = Image.open(filename)#设置图片
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)
        return redirect('/settings/picture/?upload_picture=uploaded')
    except Exception as e:
        print(e)
        return redirect('/settings/picture/')

@login_required
def save_uploaded_picture(request):#保存图片
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        filename = settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
    except Exception:
        print('hello')
    return redirect('/settings/picture/')