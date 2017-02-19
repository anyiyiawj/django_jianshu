from django import forms
from .models import Article,Topic,Notes

class NotesForm(forms.ModelForm):
    caption=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=30)
    class Meta:
        model=Notes
        fields=('caption',)
        
class ArticleForm(forms.ModelForm):
    #status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),max_length=4000) 
    class Meta:
        model=Article
        fields=('title','content')

class TopicForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=255, required=False,help_text='用空格分离标签，如“人生 爱情 哲学”')
    class Meta:
        model=Topic
        fields=('name',)