from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistationForm
from .models import Application

def index(request):
    completed_apps = Application.objects.filter(status='complited').order_by('-created_at')[:4]
    in_progress_apps = Application.objects.filter(status='in_progress').count()
    return render(request, 'main/index.html', {
        'completed_apps': completed_apps,
        'in_progress_apps': in_progress_apps,
    })
def register(request):
    if request.method == 'POST':
        form = RegistationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('index')
    else:
        form = RegistationForm()
    return render(request, 'main/register.html', {'form': form})

