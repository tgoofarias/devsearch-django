from django.shortcuts import render
from .models import Project

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', { 'projects': projects })


def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    return render(request, 'projects/single-projects.html', {'project': project, 'tags': tags})
