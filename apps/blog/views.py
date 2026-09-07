from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def post_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Okunma sayısını 1 artırır
    post.views_count += 1
    post.save(update_fields=['views_count'])

    recent_posts = Post.objects.filter(is_published=True).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/detail.html', context)