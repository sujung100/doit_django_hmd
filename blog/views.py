# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        # Post 테이블에서  category 필드를 선택안한 포스트의 갯수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context



class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        # Post 테이블에서  category 필드를 선택안한 포스트의 갯수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

    # post_list.html : class이름_list.html내부적으로 정의가 되어있기 때문에 생략가능
    # 파일명을 위에있는 규칙으로 하지않을경우 명시해줘야함
    # template_name = 'blog/post_list.html'

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)

#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#           'post': post,
#         }
#     )