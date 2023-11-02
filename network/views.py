import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import User, Post, Comment


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

    
@csrf_exempt
@login_required
def new_post(request):
    if request.method != "POST":
        return JsonResponse({
            "message": "Request method must be POST!"
        }, status=405)
    
    user = request.user
    body = request.POST.get("body")
    
    post = Post(user=user, body=body)
    post.save()
    
    formatted_timestamp = post.timestamp.astimezone(timezone.get_current_timezone()).strftime("%d-%m-%Y %H:%M:%S")
    return JsonResponse({
        "message": "Post created successfully!",
        "post": {
            "user": user.username,
            "body": body,
            "timestamp": formatted_timestamp,
            "liked_by": [],
            "comments": []
        }
    })
    
    
def get_posts(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    post_data = []
    for post in posts:
        comments = []
        for comment in post.comments.all():
            comments.append({
                'id': comment.id,
                'text': comment.body,
                'timestamp': comment.timestamp.astimezone(timezone.get_current_timezone()).strftime("%d-%m-%Y %H:%M:%S"),
                'author': comment.user.username,
            })
        post_data.append({
            'id': post.id,
            'text': post.body,
            'timestamp': post.formatted_timestamp(),
            'author': post.user.username,
            'comments': comments,
            'liked_by': [user.username for user in post.liked_by.all()],
        })
    
    return JsonResponse({
        'posts': post_data,
        'num_pages': paginator.num_pages,
        'page': page_number,
        'has_next': posts.has_next(),
        'has_previous': posts.has_previous(),
    }, safe=True)

    
@login_required
def edit_post(request):
    pass


@login_required
def create_comment(request):
    pass



def profile_page(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            'user': None,
        })
    
    is_following = False;
    if request.user.is_authenticated and request.user != user:
        is_following = request.user in user.followers.all()
        
    if request.method == "POST":
        if 'follow' in request.POST and not is_following:
            user.followers.add(request.user)
            is_following = True
        elif 'unfollow' in request.POST and is_following:
            user.followers.remove(request.user)
            is_following = False
    
            
    user_posts = Post.objects.filter(user=user).order_by('-timestamp')
    return render(request, "network/profile.html", {

        'followers': user.followers.all(),
        'following': user.following.all(),
        'bio': user.bio,
        'website': user.website,
        'profile_pic': user.profile_pic,
        'user_posts': user_posts,
        'comments': user.comments.all(),
        'liked_posts': user.liked_posts.all(),
        'is_following': is_following,
    })