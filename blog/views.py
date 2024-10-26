from lib2to3.fixes.fix_input import context

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from taggit.models import Tag

from blog.models import *
from blog.forms import *


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All posts'
        return context

def post_list(request, tag_slug=None):
    posts_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tag__in=[tag])

    paginator = Paginator(posts_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'title': 'Post List',
        'tag': tag,
    }
    return render(request, 'blog/list.html', context=context)


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post_slug,
        status=Post.Status.PUBLISHED
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # Схожі пости
    post_tags_ids = post.tag.values_list('id', flat=True)
    similar_posts = Post.published.filter(tag__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-publish')[:4]


    context = {
        'title': 'Post Detail',
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
    }
    return render(request, 'blog/detail.html', context=context)


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd['name']}`s comments: {cd['comments']}\n"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'title': 'Share post',
        'form': form,
        'sent': sent,
        'post': post,
    }
    return render(request, 'blog/share.html', context=context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'title': 'Коментарії',
        'form': form,
        'comment': comment,
        'post': post,
    }
    return render(request, 'blog/comment.html', context=context)
