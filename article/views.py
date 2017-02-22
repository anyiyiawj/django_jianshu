from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest

from django.contrib.auth.decorators import login_required

from .models import Notes,Article,Topic,ArticleComment
from .forms import NotesForm,ArticleForm,TopicForm
from activities.models import Activity,Notification

@login_required  
def article(request,article_id):
    if request.user!=Article.objects.get(id=article_id).get_author() and Article.objects.get(id=article_id).status!='p':
        return HttpResponse(status=403)#没有权限
    else:
        return render_to_response('article/article.html',{'article':Article.objects.get(id=article_id),'user':request.user,})

@login_required  
def notes(request,notes_id):
    notes=Notes.objects.get(id=notes_id)
    articles=notes.article_set.filter(status='p')
    return render_to_response('article/notes.html',{'user':request.user,'notes':notes,'articles':articles})

@login_required
def topic(request,topic_id):
    topic=get_object_or_404(Topic,id=topic_id)
    articles = topic.article_set.filter(status='p')
    return render_to_response('article/topic.html',{'user':request.user,"topic":topic,'articles':articles})

@login_required    
def add(request):
    message=''
    if  request.method=="POST":
        article=Article.objects.create(title=' ',content=' ',notes_id=1)
        return _add(request, article)
    notesform=NotesForm()
    form=ArticleForm()
    topicform=TopicForm()
    return render_to_response("article/add.html",{'user':request.user,"notesform":notesform,"form":form,"topicform":topicform,'message':message})

@login_required
def edit(request,article_id):
    article = get_object_or_404(Article, id=article_id)
    message=''
    if request.method=="POST":
        return _add(request,article)
    notesform = NotesForm(instance=article.notes)
    form = ArticleForm(instance=article)
    topicform =TopicForm(initial={'name':article.get_topics()})
    return render_to_response("article/add.html", {'user':request.user,"notesform": notesform, "form": form, "topicform": topicform,'message':message})

@login_required
def draft(request):
    draft=[]
    for article in Article.objects.filter(status='d'):
        if article.get_author()==request.user:
            print(article)
            draft.append(article)
    return render_to_response('article/draft.html',{'user':request.user,'draft':draft})
        
@login_required  
def art_delete(request,article_id):
    Article.objects.get(id=article_id).delete()
    return HttpResponseRedirect('/')
    
@login_required  
def notes_delete(request,notes_id):
    Notes.objects.get(id=notes_id).delete()
    return HttpResponseRedirect('/')    
    
@login_required
def like(request):#创建点赞和撤销点赞
    article_id = request.POST['article']
    article = Article.objects.get(pk=article_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, article=article_id,user=user) #查询该用户是否点过赞
    if like:#点过赞的撤销
        user.profile.unotify_liked(article)
        like.delete()
    else:#没有点过赞的点赞
        like = Activity(activity_type=Activity.LIKE, article=article_id, user=user)
        like.save()
        user.profile.notify_liked(article)
    return HttpResponse(str(article.calculate_likes()))#返回赞数,ajax用httpresponse，返回数据
    
@login_required
def comment(request,article_id):
    if request.method == 'POST':
        article = Article.objects.get(pk=int(article_id))
        comment = request.POST.get('comment')
        comment = comment.strip()
        if len(comment) > 0:
            article_comment = ArticleComment(user=request.user,article=article,comment=comment)
            article_comment.save()
            comm=Notification(notification_type=Notification.COMMENTED,article=article,from_user=request.user,to_user=article.get_author())
            comm.save()
        else:
            message='你填入的信息错误'
        return HttpResponseRedirect('/article/%d'%int(article_id))

@login_required
def dele_com(request,comment_id):
    comment=get_object_or_404(ArticleComment,id=comment_id)
    article=comment.article
    comment.delete()
    return HttpResponseRedirect('/article/%d'%int(article.id))



def _add(request,article):
    flag = request.POST.get('flag', None)
    if flag == "取消":
        return HttpResponseRedirect('/')
    elif flag == "发布":
        status = "p"
    elif flag == "仅自己能看":
        status = "s"
    else:
        status = "d"
    notesform = NotesForm(request.POST)
    form = ArticleForm(request.POST)
    topicform = TopicForm(request.POST)
    if form.is_valid() and topicform.is_valid() and notesform.is_valid():
        cdform = form.cleaned_data
        cdnotes = notesform.cleaned_data
        cdtopic = topicform.cleaned_data
        caption = cdnotes['caption'].strip()
        name = cdtopic['name']
        if Notes.objects.get_or_create(caption=caption)[1]:
            notes = Notes.objects.get(caption=caption)
            notes.user = request.user  # 添加外键
        else:
            notes = Notes.objects.get(caption=caption)
        notes.save()
        article.title = cdform['title']
        article.content = cdform['content']
        article.abstract = article.get_abstract()
        article.status = status
        article.notes = notes
        article.save()
        article.add_topic(name)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('你输入的东西有误')