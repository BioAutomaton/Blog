from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import PostForm, CommentForm
from .models import Post, Comment, Category


def HomeView(request):
    posts = Post.objects.order_by('-id')

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }

    return render(request, "home.html", context)


def PostDetailView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_details', pk=pk)
        else:
            return redirect('login')
    else:
        comment_form = CommentForm()

    comments = Comment.objects.filter(post=post).order_by('-id')

    paginator = Paginator(comments, 10)
    page = request.GET.get('page')

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'blog/post_details.html', context)


@login_required
def CreatePostView(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/add_post.html', context={'form': form})


@login_required
def UpdatePostView(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.user == post.author:
        if request.method == 'POST':
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post.title = post_form.cleaned_data['title']
                post.body = post_form.cleaned_data['body']
                post.snippet = post_form.cleaned_data['snippet']
                post.save()

                return redirect('post_details', pk=pk)
            else:
                return render(request, 'blog/edit_post.html',
                              context={'post': post})
        else:
            post_form = PostForm(
                initial={'title': post.title, 'body': post.body, 'category': post.category, 'snippet': post.snippet})

        context = {'post': post, 'form': post_form}
        return render(request, 'blog/edit_post.html', context)
    else:
        return HttpResponseForbidden


@login_required
def DeletePostView(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user == post.author:
        post.delete()

    return redirect('home')


class CategoriesListView(ListView):
    model = Category
    template_name = 'blog/categories_list.html'


def CategoryView(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category).order_by('-id')

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, "blog/category.html", context)


def UserProfileView(request, pk):
    profile_owner = get_object_or_404(User, id=pk)
    posts = Post.objects.filter(author=profile_owner).order_by('-id')

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "profile_owner": profile_owner,
        'posts': posts
    }

    return render(request, "blog/profile.html", context)


@login_required
def DeleteCommentView(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user == comment.author:
        comment.delete()

    return redirect(request.META.get("HTTP_REFERER"))
