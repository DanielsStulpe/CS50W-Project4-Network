import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts


def index(request):
    posts = Posts.objects.all().order_by('-date')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    for post in page_obj:
        post.is_liked_by_user = post.isLikedBy(user) if user.is_authenticated else False

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "page" : "all_posts"
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


@csrf_exempt
@login_required
def new(request):
    if request.method == "POST":
        content = request.POST["content"]
        owner = request.user

        new_post = Posts.objects.create(owner=owner, content=content)
        new_post.save()

        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "network/new.html")
    

def user_page(request, user):
    owner = User.objects.get(username=user)
    posts = Posts.objects.filter(owner=owner).order_by('-date')
    user = request.user

    followed = user in owner.followers.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        post.is_liked_by_user = post.isLikedBy(user) if user.is_authenticated else False

    return render(request, "network/user.html", {
        "owner" :  owner,
        "page_obj" : page_obj,
        "followed_by_count": owner.followed_by_count(),
        "following_count": owner.following_count(),
        "user" : user,
        "followed" : followed
    })


@login_required
def follow(request, username):
    if request.method == "POST":
        user_to_follow = User.objects.get(username=username)
        request.user.following.add(user_to_follow)
        return redirect('user_page', user=username)
    else:
        return redirect('user_page', user=username)


@login_required
def unfollow(request, username):
    if request.method == "POST":
        user_to_unfollow = User.objects.get(username=username)
        request.user.following.remove(user_to_unfollow)
        return redirect('user_page', user=username)
    else:
        return redirect('user_page', user=username)


@login_required
def following(request):
    followed_users = request.user.following.all()
    posts = Posts.objects.filter(owner__in=followed_users).order_by('-date')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        post.is_liked_by_user = post.isLikedBy(request.user)

    return render(request, "network/index.html", {
        "page_obj" : page_obj,
        "page" : "following"
    })


@csrf_exempt
@login_required
def edit(request, post_id):
    try:
        post = Posts.objects.get(owner=request.user, id=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found or unauthorized."}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            new_content = data.get("content", "").strip()
            if not new_content:
                return JsonResponse({"error": "Content cannot be empty."}, status=400)

            post.content = new_content
            post.save()
            return HttpResponse(status=204)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"error": "PUT request required."}, status=400)


@csrf_exempt
@login_required
def like(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found or unauthorized."}, status=404)

    if request.method == "POST":
        if post.isLikedBy(request.user):  # Assuming this method exists
            request.user.like.remove(post)  # Remove the like if already liked
            is_liked = False
        else:
            request.user.like.add(post)  # Add a like if not liked
            is_liked = True

        return JsonResponse({
            "is_liked": is_liked,
            "likes_count": post.likes_count()
        })
    
    return JsonResponse({"error": "POST request required."}, status=400)
