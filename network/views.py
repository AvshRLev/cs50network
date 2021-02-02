from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


from .models import User, Post, Following


class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control-sm inline',
        'placeholder': 'New Post',
        'required': 'required',
        'style':'rows: 2; padding: 4px; width: 65%; margin-left: 40px; margin-top:17px',
        'id': 'new-post-form'
        }), label=False)


def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'form': NewPostForm(),
        'page_obj': page_obj,
    })


@login_required    
def following_view(request):
    user = request.user
    user_is_following = Following.objects.all().filter(followed_by=user).values_list('user_followed', flat=True)
    posts = Post.objects.all().filter(user__in=user_is_following)
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'form': NewPostForm(),
        'page_obj': page_obj,
    })


def new_post(request):
    form = NewPostForm(request.POST)
    if form.is_valid():
        user = request.user
        content = form.cleaned_data['content']
        post = Post(user=user, content=content,)
        post.save()
    return redirect('index')


@csrf_exempt
@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return JsonResponse(post.serialize())
    else:
        return HttpResponse(status=404)
        

@csrf_exempt
@login_required
def like_handler(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)  
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            if request.user in post.users_liking.all():
                post.users_liking.remove(request.user)
                post.likes -= 1
            else:
                post.users_liking.add(request.user)
                post.likes += 1
        post.save()
        return JsonResponse(post.serialize())


@login_required
def profile(request, user):
    profile_user = User.objects.get(username=user)
    user = request.user
    try:
        following = Following.objects.get(user_followed=profile_user, followed_by=user)
    except:
        following = None
    posts = Post.objects.all().filter(user=profile_user)
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        'form': NewPostForm(),
        'following': following,
        'profile_user': profile_user,
        'page_obj': page_obj,
    })


def followship(request, profile_user):
    profile_user = User.objects.get(username=profile_user)
    user = request.user
    try:        
        followship = Following.objects.get(user_followed=profile_user, followed_by=user)
        followship.delete()        
        flag = True

    except:        
        followship = Following(user_followed=profile_user, followed_by=user)
        followship.save()        
        flag = False

    if flag == True:
        user = request.user
        followers_update = User.objects.get(username=profile_user)
        followers_update.followed_by_this_many -= 1
        followers_update.save()
        following_update = User.objects.get(username=user)
        following_update.follows_this_many -= 1 
        following_update.save()

    else:
        follower_update = User.objects.get(username=profile_user)
        follower_update.followed_by_this_many += 1
        follower_update.save()
        following_update = User.objects.get(username=user)
        following_update.follows_this_many += 1 
        following_update.save()
    
    return redirect('profile', profile_user)
    

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
