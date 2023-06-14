from .models import Comment, Post, TestModel2
from django import forms


# test
class PostFormTest(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'tag', ]


class PostFormTest2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag', ]


class TestModel2Form(forms.ModelForm):
    class Meta:
        model = TestModel2
        fields = ['hp', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',
                  ]
