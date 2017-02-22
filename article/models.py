from django.db import models
from django.contrib.auth.models import User

from activities.models import Activity

class Notes(models.Model):#文集
    user=models.ForeignKey(User,null=True)
    caption=models.CharField(max_length=50)
    create_date=models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True,blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.caption

class Topic(models.Model):#标签
    name=models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.name
        
class Article(models.Model):#文章
    STATUS_CHOICES=(
        ('d','草稿'),
        ('p','已公共发布'),
        ('s','私人文章'),
    )
    notes=models.ForeignKey(Notes)
    topic = models.ManyToManyField(Topic)
    title=models.CharField(max_length=50)
    content=models.TextField(max_length=4000)
    abstract=models.CharField(max_length=140, null=True)
    status=models.CharField(max_length=1,default='p',choices=STATUS_CHOICES)
    likes = models.IntegerField(default=0)
    create_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True,blank=True, null=True)
    
    class Meta:
        ordering=['-update_date']

    def __str__(self):
        return self.title
        
    def get_abstract(self):#得到简述
        if len(self.content) > 140:
            return self.content[:140]+'...'
        else:
            return self.content
            
    def get_author(self):#得到作者
        return self.notes.user
    
    def calculate_likes(self):#返回赞数，修改后
        likes = Activity.objects.filter(activity_type=Activity.LIKE,article=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes
        
    def get_likes(self): #得到所有这个文章的赞（而非赞数）   
        likes = Activity.objects.filter(activity_type=Activity.LIKE,article=self.pk)
        return likes

    def get_likers(self):#得到所有赞这个文章的用户
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers#得到所有赞这个文章的用户
    
    def get_comments(self):#得到评论
        return ArticleComment.objects.filter(article=self)

    def add_topic(self,name):#增加标签
        topic = name.strip()
        topic_list = topic.split(' ')
        if topic_list:
            for topic in topic_list:
                self.topic.add(Topic.objects.get_or_create(name=topic)[0])  # 增加多对多关系
        self.save()

    def get_topics(self):#得到标签长串：
        name = []
        n = self.topic.all().count()
        if n > 1:
            for topic in self.topic.all():
                name.append(topic.name)
            name = ' '.join(name)
        elif n == 1:
            for topic in self.topic.all():
                name = str(topic.name)
        else:
            name=''
        return name
        
class ArticleComment(models.Model):#文章评论
    article = models.ForeignKey(Article)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.article.title)