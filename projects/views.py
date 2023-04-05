from django.shortcuts import render

# Create your views here.
def projects(request):
    msg = 'Hello you are on the project page'
    return render(request, 'projects/projects.html', { 'message': msg })


def project(request, pk):
    return render(request, 'projects/single-projects.html', {'pk': pk})
