from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateNewUser, LoginForm, EditProfile
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from .models import UserProfile, Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from post_app.forms import PostForm
from django.contrib.auth.models import User

# Create your views here.

def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('login_app:login'))
    
    return render(request, 'login_app/sign_up.html', {'title': 'Sign Up . Instagram', 'form': form})

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('post_app:home'))

    return render(request, 'login_app/login.html', {'form': form})

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/profile.html', {'form': form})

@login_required 
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:login'))

@login_required 
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('post_app:home'))
    return render(request, 'login_app/user.html', {'form': form})

@login_required 
def user(request, username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/user_other.html', {'user_other': user_other, 'already_followed': already_followed})

@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()

    return HttpResponseRedirect(reverse('login_app:user', kwargs={'username': username}))

@login_required 
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('login_app:user', kwargs={'username': username}))