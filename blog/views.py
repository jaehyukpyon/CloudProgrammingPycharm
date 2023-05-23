from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag, Comment, TestModel1
from .forms import CommentForm

# Test
def testmodel1(request):
    post = TestModel1.objects.get(pk=1)

    context = {
        'post': post,
    }
    return render(request, 'blog/test1.html', context)

# def index(request):
#     posts = Post.objects.all().order_by('-pk');

#     return render(request, 'blog/index.html', {
#         'posts': posts
#     })

# def single_post_page(request, post_num):
#     post = Post.objects.get(pk=post_num)

#     return render(request, 'blog/single_post_page.html', {
#         'post': post,
#     })

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tag']

    template_name = 'blog/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        # LoginRequiredMixin을 override
        print('dispatch')  # 글 수정하려고 html 띄울 때, 글을 실제로 수정할 때
        if request.user.is_authenticated and self.get_object().author == request.user:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # 로그인을 안 하면 글 작성할 수 있는 페이지 접근 자체가 차단된다.
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tag']

    def test_func(self):
        # UserPassesTestMixin의 함수를 overrides
        # 글 작성 페이지를 보여줄 때, 글을 실제로 작성(post)할 때 둘다
        print('test_func')
        #return self.request.user.is_staff or self.request.user.is_superuser
        return True

    def form_valid(self, form):
        # 글을 실제로 작성할 때만 호출
        print('form_valid')
        print('is Form valid? before: ', form.is_valid()) # True


        #if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff):
        if self.request.user.is_authenticated:
            print('form', form)
            print('------------------------------')
            print('form.instance', form.instance) # form.instance pk=None, title=adfas, created_at=None
            print('type(form)', type(form)) # type(form) <class 'django.forms.widgets.PostForm'>
            print('type(form.instance)', type(form.instance)) # type(form.instance) <class 'blog.models.Post'>
            form.instance.author = self.request.user
            print('is Form valid? after: ', form.is_valid())
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

    def get_context_data(self, *, object_list=None, **kwargs):
        # 글 작성을 위한 form(html)을 보여줄때만 호출
        print('get_context_data')
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        return context


# class PostCreate(CreateView):
#     model = Post
#     fields = ['title', 'content', 'head_image', 'file_upload', 'author', 'category', 'tag']

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PostCreate, self).get_context_data()
#         context['categories'] = Category.objects.all()
#         context['no_category_count'] = Post.objects.filter(category=None).count()
#         return context

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()
        return context


def categories_page(request, slug):
    if slug == 'no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None).order_by('-pk')
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category).order_by('-pk')

    context = {
        'category': category,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_count': Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'tag': tag,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_count': Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


def add_comment(request, pk):
    if not request.user.is_authenticated:
        raise PermissionError

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        comment_form = CommentForm(data=request.POST)
        comment_temp = comment_form.save(commit=False)
        comment_temp.post = post
        comment_temp.author = request.user
        comment_temp.save()

        return redirect(post.get_absolute_url())
    else:
        raise PermissionError
