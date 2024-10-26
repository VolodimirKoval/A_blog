from django.urls import path
from blog.views import *


app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('posts-by-tags/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    # path('', PostListView.as_view(), name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post_detail, name='post_detail'),
    path('post-share/<int:post_id>/', post_share, name='post_share'),
    path('post-comment/<int:post_id>/', post_comment, name='post_comment'),
]