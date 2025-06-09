from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import StudentRegistrationForm
from django.contrib import messages
from .models import StudentProfile
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileEditForm


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()
            
            if not hasattr(user, 'studentprofile'):  # This checks for existing profile
                StudentProfile.objects.create(
                    user=user,
                    school=form.cleaned_data['school'],
                    grade_level=form.cleaned_data['grade_level'],
                    town=form.cleaned_data['town'],
                    birthdate=form.cleaned_data.get('birthdate')  # Handles null automatically
                )
            
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error with your registration.")
            print(form.errors)
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "!", f"Welcome back, {user.username}!")
            return redirect('home')
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def dashboard(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        # Handle case where profile doesn't exist
        profile = None
    
    # Get task statistics
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    
    # Difficulty breakdown
    difficulty_stats = {
        'easy': tasks.filter(difficulty='E').count(),
        'medium': tasks.filter(difficulty='M').count(),
        'hard': tasks.filter(difficulty='H').count()
    }
    
    context = {
        'student': request.user,
        'profile': profile,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'difficulty_stats': difficulty_stats
    }
        
    return render(request, 'dashboard.html', context)



@login_required
def edit_profile(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Profile not found")
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentProfileEditForm(instance=profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile': profile
    })