from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    # path('<int:pk>/', views.single_post_page),

    # /blog/
    path('', views.PostList.as_view(), name='post_list'),
    # /blog/1/
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),


    path('category/<str:slug>/', views.category_page, name='category_filter'),
    # /blog/category/{self.slug}/
    # /blog/category/파이썬

]