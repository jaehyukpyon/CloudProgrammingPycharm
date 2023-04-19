from django.shortcuts import render
from blog.models import Post

# Create your views here.

def main(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    context = {
        'recent_posts': recent_posts,
    }
    return render(request, 'single_pages/main.html', context)


def test(request, pk):
    print('pk=', pk)

    return render(request, 'single_pages/test.html')