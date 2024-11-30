from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm, CommentForm
from django.core.paginator import Paginator


def post_list(request):
    # Отримуємо параметр для фільтрації за тегом
    tag_filter = request.GET.get('tag')

    post_list = Post.objects.all().order_by('-created_at')

    # Фільтрація за тегами, якщо параметр присутній
    if tag_filter:
        post_list = post_list.filter(tags__name=tag_filter)

    paginator = Paginator(post_list, 5)  # 5 постів на сторінку
    page_number = request.GET.get('page')  # Отримуємо номер сторінки з запиту
    posts = paginator.get_page(page_number)  # Отримуємо сторінку з постами

    # Отримуємо всі теги для фільтрації
    tags = Tag.objects.all()

    return render(request, 'blog/post_list.html', {'posts': posts, 'tags': tags, 'tag_filter': tag_filter})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comments})

def post_list_by_tag(request, tag):
    # Фільтруємо пости за тегом
    posts = Post.objects.filter(tags__name=tag).order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts, 'tag': tag})
