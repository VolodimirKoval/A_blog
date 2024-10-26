
from django import template
from django.db.models import Count
from django.template import Library

from blog.models import Post, Comment

register: Library = template.Library()


@register.simple_tag(name='total_posts')
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/latest-posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag()
def get_most_comments_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).exclude(total_comments=0).order_by('-total_comments')[:count]
