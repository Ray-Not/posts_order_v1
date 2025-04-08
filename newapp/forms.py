from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'CategoryType', 'categories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['CategoryType'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['categories'].widget.attrs.update(
            {'class': 'form-control'}
        )
