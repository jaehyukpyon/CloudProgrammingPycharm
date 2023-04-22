from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Test
class TestModel1(models.Model):
    # must defind a  'max_length' attribute
    name = models.CharField(max_length=10)
    hp = models.IntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


# Create your models here.
class Post(models.Model):
    # 현재 상태로는, title, content, author만 넣어주면 create 함수가 잘 동작해서 db에 잘 저장된다.
    title = models.CharField(max_length=30)

    # content = models.TextField()
    content = MarkdownxField()

    head_image = models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d')
    # head_image = models.ImageField(blank=True)

    file_upload = models.FileField(blank=True, upload_to='blog/files/%Y/%m/%d')

    # 생성일자는 auto_now_add를 사용
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 수정일자는 auto_now를 사용
    updated_at = models.DateTimeField(auto_now=True)

    # not null contraint failed: author_id
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # tag를 지운다고 해서 post 에 영향이 갈 필요가 없다. 기본으로 null=True
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        # return f'pk={self.pk}, title={self.title}, created_at={self.created_at}, author={self.author}'
        return f'pk={self.pk}, title={self.title}, created_at={self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

