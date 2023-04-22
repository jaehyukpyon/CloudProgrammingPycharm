from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',
                  ]

class PostFormTest(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'tag', ]

class PostFormTest2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag', ]