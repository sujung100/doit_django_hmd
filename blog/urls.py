from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    # path('<int:pk>/', views.single_post_page),

    # /blog/
    path('', views.PostList.as_view(), name='post_list'),
    # /blog/1/
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),

    # /blog/category/{self.slug}/
    # /blog/category/파이썬
    path('category/<str:slug>/', views.category_page, name='category_filter'),

    path('tag/<str:slug>/', views.tag_page, name='tag_filter'),

    path('create_post/', views.PostCreate.as_view(), name='create_post'),

    path('search/<str:q>/', views.PostSearch.as_view()),

    # /blog/update_post/페이지
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update_post'),

    path('<int:pk>/new_comment/', views.new_comment),

    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),

    path('delete_comment/<int:pk>/', views.delete_comment),
]