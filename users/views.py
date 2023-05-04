from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import search_profiles, pagination_profiles
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username, password = request.POST['username'].lower(), request.POST['password']
        try:
            user = User.objects.get(username=username)           
        except:
            messages.error(request, 'Username does not exists')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Wrong password')

    context = {
        'page': 'login'
    }
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'User was successfully logged out!')
    return redirect('login')


def register_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User created succesfully')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occurred.')

    context = {
        'page': 'register',
        'form': form
    }
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = search_profiles(request)
    custom_range, profiles = pagination_profiles(request, profiles, 3)
    context = { 'profiles': profiles, 'custom_range': custom_range, 'search_query': search_query }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = { 'profile': profile }
    return render(request, 'users/user-profile.html', context)


def user_account(request):
    if not request.user.is_authenticated:
        redirect('profiles')
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    form = SkillForm(instance=skill)
    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted')
        return redirect('account') 
    context = {
        'object': skill
    }
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    inbox_messages = profile.messages.all()
    unread_count = inbox_messages.filter(is_read=False).count()
    context = {
        'inbox_messages': inbox_messages,
        'unread_count': unread_count
    }
    return render(request, 'users/inbox.html', context)



@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {
        'message': message
    }
    return render(request, 'users/message.html', context)


@login_required(login_url='login')
def create_message(request, pk):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.name = request.user.profile.name
            message.email = request.user.profile.email
            message.sender = request.user.profile
            message.recipient = Profile.objects.get(id=pk)
            message.save()
            return redirect('user-profile', pk=pk)

    recipient = Profile.objects.get(id=pk)
    context = {
        'form': form,
        'recipient': recipient,
    }
    return render(request, 'users/message_form.html', context)