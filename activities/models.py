from django.contrib.auth.models import User
from django.db import models
from django.utils.html import escape

class Activity(models.Model):
    FAVORITE = 'F'#文集
    LIKE = 'L'#文章
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        )
    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    article = models.IntegerField(null=True, blank=True)
    notes=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.activity_type
   
class Notification(models.Model):
    LIKED = 'L'
    COMMENTED = 'C'
    FAVORITED = 'F'
    NOTESCOMMENTED = 'N'
    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (FAVORITED, 'Favorited'),
        (NOTESCOMMENTED, 'NotesCommented'),
        )
    _LIKED_TEMPLATE = '<a href="/people/{0}/">{1}</a> 喜欢你的文章： <a href="/article/{2}/">{3}</a>'
    _COMMENTED_TEMPLATE = '<a href="/people/{0}/">{1}</a> 评论了你的文章：<a href="/article/{2}/">{3}</a>'
    _FAVORITED_TEMPLATE = '<a href="/people/{0}/">{1}</a> 喜欢你的文集： <a href="/notes/{2}/">{3}</a>'
    _NOTESCOMMENTED_TEMPLATE = '<a href="/people/{0}/">{1}</a> 评论了你的文集：<a href="/notes/{2}/">{3}</a>'

    from_user = models.ForeignKey(User, related_name='+')#动作发起者
    to_user = models.ForeignKey(User, related_name='+')#动作接受者，reuqest.user
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('article.Article', null=True, blank=True)
    notes=models.ForeignKey('article.Notes',null=True,blank=True)
    notification_type = models.CharField(max_length=1,choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)#是否被阅读
    class Meta:
        ordering=('-date',)
    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                self.from_user.id,
                escape(self.from_user.username),
                self.article.id,
                escape(self.article.title)
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                self.from_user.id,
                escape(self.from_user.username),
                self.article.id,
                escape(self.article.title)
                )
        elif self.notification_type == self.FAVORITED:
            return self._FAVORITED_TEMPLATE.format(
                self.from_user.id,
                escape(self.from_user.username),
                self.notes.id,
                escape(self.notes.caption)
                )
        elif self.notification_type == self.NOTESCOMMENTED:
            return self._NOTESCOMMENTED_TEMPLATE.format(
                self.from_user.id,
                escape(self.from_user.username),
                self.notes.id,
                escape(self.notes.caption)
                )
        else:
            return 'Ooops! Something went wrong.'