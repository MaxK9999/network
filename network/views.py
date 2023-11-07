from email import message
import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import User, Post, Comment, Follower


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
    image = request.FILES.get("image")
    
    post = Post(user=user, body=body, image=image)
    post.save()
    
    formatted_timestamp = post.timestamp.astimezone(timezone.get_current_timezone()).strftime("%d-%m-%Y %H:%M:%S")
    
    new_post_data = {
        'id': post.id,
        'text': post.body,
        'image': post.image.url if post.image else None,
        'timestamp': post.formatted_timestamp(),
        'author': user.username,
        'comments': [],
        'liked_by': [],
        'is_author': True,
    }
    
    return JsonResponse({
        "message": "Post created successfully!",
        "post": new_post_data
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
            
        is_author = post.user == request.user
        image_url = post.image.url if post.image else None
        
        post_data.append({
            'id': post.id,
            'text': post.body,
            'image': image_url,
            'timestamp': post.formatted_timestamp(),
            'author': post.user.username,
            'comments': comments,
            'liked_by': [user.username for user in post.liked_by.all()],
            'is_author': is_author,
        })
    
    return JsonResponse({
        'posts': post_data,
        'num_pages': paginator.num_pages,
        'page': page_number,
        'has_next': posts.has_next(),
        'has_previous': posts.has_previous(),
    }, safe=True)

    
@login_required
def edit_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({
            "message": "Request method must be POST!"
        }, status=405)
    
    data = json.loads(request.body)
    edited_text = data.get("text")
    
    try:
        post = Post.objects.get(id=post_id)
        if post.user != request.user:
            return JsonResponse({
                "message": "You can only edit your own posts!",
            }, status=403)
        post.body = edited_text
        post.save()
        
        is_author = post.user == request.user
        return JsonResponse({
            "message": "Post edited successfully!",
            "post": {
                "id": post.id,
                "text": post.body,
                "timestamp": post.formatted_timestamp(),
                "liked_by": [user.username for user in post.liked_by.all()],
                "comments": [],
                "author": post.user.username,
                "is_author": is_author,
            }
        })
    except Post.DoesNotExist:
        return JsonResponse({
            "message": "Post does not exist!",
        }, status=404)
        
        
@require_http_methods(["DELETE"])
@login_required
def delete_post(request, post_id):   
    try:
        post = Post.objects.get(id=post_id)
        if post.user != request.user:
            return JsonResponse({
                "message": "You can only delete your own posts!",
            }, status=403)
        post.delete()
        return JsonResponse({
            "message": "Post deleted successfully!",
        })
    except Post.DoesNotExist:
        return JsonResponse({
            "message": "Post does not exist!",
        }, status=404)


        
@login_required
def create_comment(request):
    pass


def profile_page(request, username):
    current_user = request.user
    user = User.objects.get(username=username)
    is_followed = False
    if current_user.is_authenticated:
        is_followed = user.is_followed_by(current_user)
        
    follower_count = Follower.objects.filter(user_to=user).count()
    following_count = Follower.objects.filter(user_from=user).count()
   
    return render(request, "network/profile.html", {
        'current_user': current_user.username,
        'username': user.username,
        'bio': user.bio,
        'website': user.website,
        'is_followed': is_followed,
        'follower_count': follower_count,
        'following_count': following_count,
    })
    

@login_required
def follow(request, username):
    if request.user.is_authenticated:
        current_user = request.user
        target_user = User.objects.get(username=username)

        if target_user != current_user:
            if target_user.is_followed_by(current_user):
                Follower.objects.filter(user_from=current_user, user_to=target_user).delete()
                message = 'Unfollowed'
            else:
                Follower(user_from=current_user, user_to=target_user).save()
                message = 'Followed'
        else:
            message = 'You cannot follow yourself'
        
        return JsonResponse({
            'message': message,
        })


@login_required
def following_page(request):
    current_user = request.user
    
    return render(request, "network/following.html", {
        'current_user': current_user.username,
    })


@login_required
def following_posts(request):
    current_user = request.user
    following = Follower.objects.filter(user_from=current_user).values_list('user_to', flat=True)
    
    if not following:
        return JsonResponse({
            'message': 'You are not following anyone!',
        }, safe=True)
    
    posts = Post.objects.filter(user__in=following).order_by("-timestamp")
    posts_per_page = 10
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    
    post_data = []    
    for post in page_posts:
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
        'posts': post_data
    }, safe=True)
    
    
def get_user_posts(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by("-timestamp")
    posts_per_page = 10
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    post_data = []
    for post in page_posts:
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
        'posts': post_data
    }, safe=True)


@login_required 
def like_posts(request, post_id):
    if request.method != "POST":
        return JsonResponse({
            "message": "Request method must be POST!"
        }, status=405)
    
    post = Post.objects.get(id=post_id)
    current_user = request.user
    
    if current_user in post.liked_by.all():
        post.liked_by.remove(current_user)
        message = 'Unliked'
    else:
        post.liked_by.add(current_user)
        message = 'Liked'
    
    return JsonResponse({
        "message": message,
    })