from django.shortcuts import render, redirect
from .models import *
from .forms import PostForm


def index(request):
    return render(request, 'index.html')


def posts(request):
    if request.user.is_superuser:
        all_posts = Post.objects.all()
        context = {'all_posts': all_posts}
        return render(request, 'posts.html', context=context)

    current_user = myUser.objects.get(myUserBase=request.user)
    # print("current user: ", current_user)
    all_users = myUser.objects.all()
    # print(all_users)

    not_blocked = []
    for user in all_users:
        # print(current_user.is_blocked(user))
        if not current_user.is_blocked(user):
            not_blocked.append(user)

    # print(not_blocked)
    posts_not_blocked = []
    for user in not_blocked:
        posts_from_user = Post.objects.filter(author=user).all()
        for p in posts_from_user:
            posts_not_blocked.append(p)

    context = {'posts': posts_not_blocked}

    return render(request, 'posts.html', context=context)


def addpost(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = myUser.objects.get(myUserBase=request.user)
            post.save()
            return redirect('/posts/')
    if request.method == 'GET':
        context = {'add_post_form': PostForm}
        return render(request, 'addpost.html', context=context)


def profile(request):
    this_user = myUser.objects.get(myUserBase=request.user)
    this_user_posts = Post.objects.filter(author=this_user).all()
    context = {'user': this_user, 'posts': this_user_posts}
    return render(request, 'profile.html', context=context)


def blockedusers(request):
    this_user = myUser.objects.get(myUserBase=request.user)
    all_users = myUser.objects.all()

    blocked_users = []
    for user in all_users:
        # print(current_user.is_blocked(user))
        if this_user.is_blocked(user):
            blocked_users.append(user)

    print(blocked_users)
    context = {'blocked': blocked_users}

    return render(request, 'blockedUsers.html', context=context)
