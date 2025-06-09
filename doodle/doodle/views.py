from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from accounts.models import StudentProfile
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def home(request):
    print("Home view called")  
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

# def contact(request):
#     if request.method == 'POST': 
#         form = ContactForm(request.POST)
#         if form.is_valid(): 
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
        
#             send_mail(
#                 subject=f'New Contact Form Submission from {name}', 
#                 message=message, 
#                 from_email=email, #sender email 
#                 recipient_list=['sandy.laine6@gmail.com'],
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Your message has been sent successfully!')
#             return redirect('contact')
#     else: 
#         form = ContactForm()
        
#     return render(request, 'contact.html', {'form':form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Simulate success without sending email
            print("Form is valid. Name:", form.cleaned_data['name'])
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def register(request):
    return render(request, 'accounts/register.html')


@login_required
def dashboard(request):
    student = request.user
    # profile = StudentProfile.objects.get(user=student)
    profile = StudentProfile.objects.get_or_create(user=request.user)
    
    # Task statistics
    total_tasks = Task.objects.filter(user=student).count()
    completed_tasks = Task.objects.filter(user=student, completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    
    # Difficulty breakdown
    difficulty_stats = {
        'easy': Task.objects.filter(user=student, difficulty='E').count(),
        'medium': Task.objects.filter(user=student, difficulty='M').count(),
        'hard': Task.objects.filter(user=student, difficulty='H').count()
        }
    
    context = {
        'student': student,
        'profile': profile,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'difficulty_stats': difficulty_stats,
    }
    return render(request, 'dashboard.html', context)