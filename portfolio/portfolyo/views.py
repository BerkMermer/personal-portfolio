from django.conf import settings
from django.shortcuts import render
from .models import Project
from .forms import ContactForm
from .seed import ensure_seed_projects, seed_projects_as_display

def project_list(request):
    projects = []
    try:
        ensure_seed_projects()
        projects = list(Project.objects.all())
    except Exception:
        projects = []
    if not projects:
        projects = seed_projects_as_display()
    form = ContactForm()
    return render(request, 'project_list.html', {
        'projects': projects,
        'form': form,
        'formspree_url': settings.FORMSPREE_URL,
    })
