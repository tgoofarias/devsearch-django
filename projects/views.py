from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import search_projects, pagination_projects
from .models import Project
from .forms import ProjectForm, ReviewForm

# Create your views here.
def projects(request):
    projects, search_query = search_projects(request)
    custom_range, projects = pagination_projects(request, projects, 3)
    context = { 'projects': projects, 'search_query': search_query, 'custom_range': custom_range }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = project.tags.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.project = project
                review.owner = request.user.profile
                review.save()
                project.get_vote_count
                messages.success(request, 'Your review was succesfully submitted')
                return redirect('project', pk=project.id)
    
    return render(request, 'projects/single-project.html', {'project': project, 'tags': tags, 'form': form})


@login_required(login_url='login')
def create_project(request):
    if request.method == 'GET':
        form = ProjectForm()
        context = {'forms': form}
        return render(request, 'projects/project_form.html', context)
    elif request.method == 'POST':
        profile = request.user.profile
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'forms': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'GET':
        return render(request, 'delete_template.html', {'object': project})
    if request.method == 'POST':
        project.delete()
        return redirect('projects')