from django.db import models
from django.contrib.auth.models import User

from activities.models import Notification

class Profile(models.Model):
    user=models.OneToOneField(User)
    STATUS_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )
    gender= models.CharField(max_length=1,choices=STATUS_CHOICES)
    picture = models.ImageField(upload_to='profile_images',null=True,blank=True)
    signature=models.CharField(max_length=50,null=True,blank=True)
    views = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=50,null=True, blank=True)
    def __str__(self):
        return self.user.username
        
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