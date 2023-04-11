from django.shortcuts import render, redirect
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


def create_project(request):
    if request.method == 'GET':
        form = ProjectForm()
        context = {'forms': form}
        return render(request, 'projects/project_form.html', context)
    elif request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')


def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'forms': form}
    return render(request, 'projects/project_form.html', context)


def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'GET':
        return render(request, 'projects/delete_template.html', {'project': project})
    if request.method == 'POST':
        project.delete()
        return redirect('projects')