from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Post, Category, Comment
from .forms import  CommentForm
from shop.models import UserProfile

def blog_get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2
    return {'cats1': all[:half], 'cats2': all[half:]}


def blog(request):
    posts = Post.objects.all().order_by('-published_date')
    categories = Category.objects.all()
    context = {'posts': posts, 'categories': categories}
    context.update(blog_get_categories())
    return render(request, "blog/index.html", context)

def blog_post(request, title):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    post = get_object_or_404(Post, slug=title)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post', title=title)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'profile': profile,
        'user': request.user

    }
    context.update(blog_get_categories())
    return render(request, "blog/post.html", context)

def blog_category(request, name):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {'posts': posts}
    context.update(blog_get_categories())
    return render(request, "blog/index.html", context)


def blog_search(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)) if query else []
    context = {'posts': posts, 'query': query}
    context.update(blog_get_categories())
    return render(request, "blog/index.html", context)
