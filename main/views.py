from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistrationForm, ApplicationForm, CategoryForm, InProgressForm, CompletedForm
from .models import Application, Category, CustomUser


def index(request):
    completed_apps = Application.objects.filter(status='complited').order_by('-created_at')[:4]
    in_progress_apps = Application.objects.filter(status='in_progress').count()
    return render(request, 'main/index.html', {
        'completed_apps': completed_apps,
        'in_progress_apps': in_progress_apps,
    })
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_superuser:
        return redirect('admin_panel')
    status_filter = request.GET.get('status')
    apps = Application.objects.filter(user=request.user).order_by('-created_at')
    if status_filter:
        apps = apps.filter(status=status_filter)
    return render(request, 'main/profile.html', {'apps': apps, 'current_stastus': status_filter})

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            return redirect('profile')
    else:
        form = ApplicationForm()
    return render(request, 'main/create_app.html', {'form': form})

@login_required
def delete_application(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if app.status != 'new':
        return redirect('profile')
    if request.method == 'POST':
        app.delete()
        return redirect('profile')
    return render(request, 'main/delete_app.html', {'app': app})

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_panel(request):
    apps = Application.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    users = CustomUser.objects.filter(is_superuser=False)
    if request.method == 'POST':
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            cat = cat_form.save()
            return redirect('admin_panel')
    else:
        cat_form = CategoryForm()
    return render(request, 'main/admin_panel.html', {'apps': apps, 'categories': categories, 'cat_form': cat_form,})

@user_passes_test(is_admin)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('admin_panel')

@user_passes_test(is_admin)
def delete_application_admin(request, pk):
    app = get_object_or_404(Application, pk=pk)
    app.delete()
    return redirect('admin_panel')

@user_passes_test(is_admin)
def change_status(request, pk, new_status):
    app = get_object_or_404(Application, pk=pk)
    if app.status != 'new':
        return redirect('admin_panel')

    FormClass = InProgressForm if new_status == 'in_progress' else CompletedForm
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            app.status = new_status
            app.save()
            return redirect('admin_panel')
    else:
        form = FormClass(instance=app)

    return render(request, 'main/change_status.html', {'form': form, 'app': app, 'new_status': new_status})