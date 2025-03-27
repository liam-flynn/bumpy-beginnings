from django import forms
from .models import Article
from tinymce.widgets import TinyMCE

# form used my admins to create new articles in CMS


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'subtitle', 'text',
                  'source', 'related_week', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Article Title'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Article subtitle'
            }),
            'text': TinyMCE(attrs={
                'cols': 80, 'rows': 10, 'class': 'w-full border border-gray-300 rounded-lg py-2 px-4 shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500'
            }),
            'source': forms.URLInput(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Article source URL'
            }),
            'related_week': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
            })
        }
