from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm

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

# superuser 또는 staff만 포스트를 작성할 수 있게 만들기
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    form_class = PostForm
    # template_name 생략가능하다(이름을 이렇게 줬기때문에 내부적으로 알아서 읽음)
    template_name = 'blog/post_form.html'

    # 페이지 접근 권한을 부여한다(superuser 또는 staff)
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    # 로그인한 사용자가 superuser 또는 staff일때, 동작하게하기
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            # input 요소에 입력된 값을 가져오기 위한 기능추가(tag)
            response = super(PostCreate, self).form_valid(form)
        
            tags_str = self.request.POST.get('tags_str')
            # tag_str로 받은 값의 쉼표를 세미콜론으로 모두 변경하고, 세미콜론으로 split 해서 리스트형태로 tags_list에 담는다
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                # tags_list의 문자열형태의 리스트 -> Tag모델의 인스턴스로 변환
                for t in tags_list:
                    # 앞뒤 공백 제거
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    # slug 값 생성
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        else:
            return redirect('/blog/')


class PostDetail(DetailView): 
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        # Post 테이블에서  category 필드를 선택안한 포스트의 갯수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context



class PostList(ListView):
    model = Post
    ordering = '-pk'
    # 한 페이지당 보여줄 post 갯수 설정
    paginate_by = 3

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


class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context

# post 수정페이지 구현
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    # summernote로 update form구현
    form_class = PostForm

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context
    
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        

# 로그인한상태로 댓글쓰기허용
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied
        
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied