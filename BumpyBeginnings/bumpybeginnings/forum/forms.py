from django import forms
from .models import Forum, Post, Comment
from tinymce.widgets import TinyMCE

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['forumName', 'description', 'isLive']
        widgets = {
            'forumName': forms.TextInput(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500', 
                'placeholder': 'Enter forum name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter description',
                'rows': 4
            }),
            'isLive': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-sky-600 border-gray-300 focus:ring-sky-500'
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postTitle', 'postText']
        widgets = {
            'postTitle': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg py-2 px-4 shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500'}),
            'postText': TinyMCE(attrs={'cols': 80, 'rows': 10, 'class': 'w-full border border-gray-300 rounded-lg py-2 px-4 shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentText']
        widgets = {
            'commentText': TinyMCE(attrs={'rows': 3}),
        }