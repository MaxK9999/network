import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
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
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get('body')
        if body:
            user = request.user
            post = Post.objects.create(
                user=user,
                body=body,
            )
            return JsonResponse({
                "message": "Post created succesfully!"
                })
        else:
            return JsonResponse({
                "message": "Cannot post an empty message."
            })
    else:
        return JsonResponse({
            "message": "POST request required"
        })


@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_body = data.get('body')
        post = Post.objects.get(pk=post_id)
        if post.user == request.user and new_body:
            post.body = new_body
            post.save()
            return JsonResponse({
                "message": "Post edited succesfully."
            })
        else:
            return JsonResponse({
                "message": "Permission denied and/or body content is missing."
            })
    else:
        return JsonResponse({
            "message": "Post request required!"
        })


@csrf_exempt
@login_required
def create_comment(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        image = request.FILES.get('image')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({
                "message": "Post not found"
            })
        
        if content or image:
            comment = Comment(user=request.user, post=post, content=content)
            if image:
                comment.image = image
            comment.save()
            return JsonResponse({
                "message": "Comment created succesfully"
            })
        else:
            return JsonResponse({
                "message": "Comment content is missing"
            })
    return JsonResponse({
        "message": "POST request required"
    })
    

def all_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'index.html', {
        'posts': posts
    })