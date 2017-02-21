from django.db import models
from django.contrib.auth.models import User

from activities.models import Notification
from zt import settings

import hashlib
import urllib
import os

class Profile(models.Model):
    user=models.OneToOneField(User)
    STATUS_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )
    gender= models.CharField(max_length=1,choices=STATUS_CHOICES)
    signature=models.CharField(max_length=50,null=True,blank=True)
    views = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=50,null=True, blank=True)
    def __str__(self):
        return self.user.username

    def get_picture(self):#个人图片地址
        no_picture = 'http://127.0.0.1:8000/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
        except Exception:
            return no_picture

    def get_article(self):#下属文章
        article=[]
        for notes in self.user.notes_set.all():
            article.extend(notes.article_set.all())
        return article
        
    def notify_liked(self, article):#创建通知
        if self.user!=article.notes.user:
            Notification(notification_type=Notification.LIKED,from_user=self.user,to_user=article.notes.user,article=article).save()

    def unotify_liked(self,article):#撤回通知  
        if self.user!=article.notes.user:
            Notification.objects.filter(notification_type=Notification.LIKED,from_user=self.user,to_user=article.notes.user,article=article).delete()


    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,from_user=self.user, to_user=feed.user,feed=feed).save()

    def follow(self,user):
        Follow.objects.create(ed_profile=user.profile,ing_profile=self)

    def unfollow(self,user):
        Follow.objects.get(ed_profile=user.profile,ing_profile=self).delete()

    def is_following(self,user):#是否关注他
        if Follow.objects.filter(ed_profile=user.profile, ing_profile=self):
            return True
        else:
            return False

    def is_followed(self,user):#是否被关注
        if Follow.objects.filter(ed_profile=self, ing_profile=user.profile):
            return True
        else:
            return False

    def get_follower(self):#得到关注者
        return Follow.objects.filter(ed_profile=self).all()

    def get_following(self):#得到我关注的人
        return Follow.objects.filter(ing_profile=self).all()



class Follow(models.Model):
    ed_profile = models.ForeignKey(Profile, related_name='+')  # 被关注者
    ing_profile = models.ForeignKey(Profile, related_name='+')  # 关注者
    time = models.DateTimeField(auto_now_add=True)