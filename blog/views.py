from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from .forms import PostForm

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


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    form_class = PostForm
    # template_name 생략가능하다(이름을 이렇게 줬기때문에 내부적으로 알아서 읽음)
    template_name = 'blog/post_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


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

# 방법1
# def category_page(request, slug):
#     # 비어있는 딕셔너리 변수 선언
#     context = {}
#     # 선택한 슬러그에 해당하는 Category테이블의 레코드를 가져옴
#     category = Category.objects.get(slug=slug)
#     # post 테이블에서 선택한 category의 레코드만 필터링
#     context['post_list'] = Post.objects.filter(category=category)
#     # Category 테이블의 목록 모두 가져옴
#     context['categories'] = Category.objects.all()
#     # Post 테이블에서  category 필드를 선택안한 포스트의 갯수
#     context['no_category_post_count'] = Post.objects.filter(category=None).count()
#     # 선택한 카테고리의 레코드
#     context['category'] = category
#     # print(context)

#     return render(
#         request,
#         'blog/post_list.html',
#         context
#     )


# 방법2
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        # 선택한 슬러그의 해당하는 Category테이블의 레코드
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
        # Post 테이블에서 선택한 category의 레코드만 필터링

    context = {
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_cnt': Post.objects.filter(category=None).count(),
        'category': category
    }
    # print(context)
    return render(request,'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag' : tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )