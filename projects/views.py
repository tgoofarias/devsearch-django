from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', { 'projects': projects })


def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    return render(request, 'projects/single-project.html', {'project': project, 'tags': tags})


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