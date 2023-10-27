import json
from django.contrib.auth import authenticate, login, logout
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
    
    return JsonResponse({
        "message": "Post created succesfully!"
    })
    

def load_posts(request):
    posts = Post.objects.annotate(like_count=F('liked_by')).order_by('-timestamp')
    
    post_data = [{
            "id": post.id,
            "user": post.user,
            "body": post.body,
            "image": post.image,
            "timestamp": post.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked_by": [user.username for user in post.liked_by.all()],
            "comments": post.comments,
    } for post in posts]
    
    return JsonResponse(post_data, safe=False)


@csrf_exempt
@login_required
def edit_post(request):
    pass


@csrf_exempt 
@login_required
def create_comment(request):
    pass
