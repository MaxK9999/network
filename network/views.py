import json
from tkinter import Pack
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

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
        })
    
    user = request.user
    body = request.POST.get("body")
    image = request.POST.get("image")
    
    post = Post(user=user, body=body, image=image)
    post.save()
    
    return JsonResponse({
        "message": "Post created succesfully!"
    })
    

def load_posts(request):
    posts = Post.objects.select_related('user').prefetch_related('liked_by').order_by('-timestamp')

    items_per_page = 10
    paginator = Paginator(posts, items_per_page)
    page = request.GET.get('page')
    
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    
    post_data= []
    for post in posts_page:
        post_item = {
            "id": post.id,
            "user": post.user,
            "body": post.body,
            "image": post.image,
            "timestamp": post.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked_by": [user.username for user in post.liked_by.all()],
            "comments": post.comments,
        }
        post_data.append(post_item)
    
    return JsonResponse({
        "posts": post_data,
        "has_next": posts_page.has_next(),
        })


@csrf_exempt
@login_required
def edit_post(request):
    pass


@csrf_exempt 
@login_required
def create_comment(request):
    pass
