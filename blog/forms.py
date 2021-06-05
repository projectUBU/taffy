from django import forms
from .models import Post,Comment
from app.models import Profile


        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','image']

        widgets = {
        
            'title': forms.Textarea(attrs={'class': 'editable medium-editor-textarea','style':'font-weight: bold; font-size: 150%;','rows':'3' ,'cols':'30'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {

         'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea','style':'font-size: 100%;','rows':'10' ,'cols':'40'})
        
      }