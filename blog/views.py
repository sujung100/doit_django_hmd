# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')

#     return render(
#         request,
#         'blog/index.html',
#         {
#           'posts' : posts
#         }
#     )

class PostDetail(DetailView):
    model = Post

class PostList(ListView):
    model = Post
    ordering = '-pk'
    # post_list.html : class이름_list.html내부적으로 정의가 되어있기 때문에 생략가능
    # 파일명을 위에있는 규칙으로 하지않을경우 명시해줘야함
    # template_name = 'blog/post_list.html'

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
          'post': post,
        }
    )