from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by("-created_at")

    return render(request, "network/index.html", {
        "posts": posts
    })


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

def create_post(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method == 'POST':
        content = request.POST['content']
        new_post = Post(content=content, user=user)
        new_post.save()

        return HttpResponseRedirect(reverse("index"))

def like_post(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = Post.objects.get(pk=post_id)

        liked_post = Like.objects.filter(user=user, post=post).first()

        if liked_post:
            liked_post.delete()
        else:
            like = Like(user=user, post=post)
            like.save()

        likes_count = post.likes.count()

    return HttpResponseRedirect(reverse("index"))

def profile_view(request, username):
    user = User.objects.get(username=username)
    is_following = Follow.objects.filter(following=user)
    
    return render(request, "network/profile.html", {
        "user": user,
        "is_following": is_following
    })


def follow(request, user_id):
    if request.method == 'POST':
        user = request.user

        if not user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        if user.id == user_id:
            return HttpResponseRedirect(reverse("profile"))

        following_user = User.objects.get(pk=user_id)

        follow_exists = Follow.objects.filter(user=user, following=following_user).exists()
        if follow_exists:
            Follow.objects.filter(user=user, following=following_user).delete()
        else:         
            follow = Follow(user=user, following=following_user)
            follow.save()   


        return HttpResponseRedirect(reverse("profile", args=(following_user,)))
