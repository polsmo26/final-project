from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from accounts.models import StudentProfile
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings

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

# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             # Simulate success without sending email
#             print("Form is valid. Name:", form.cleaned_data['name'])
#             messages.success(request, 'Your message has been sent successfully!')
#             return redirect('contact')
#     else:
#         form = ContactForm()
    
#     return render(request, 'contact.html', {'form': form})


def contact(request):
    print(f"Contact view called with method: {request.method}")
    if request.method == 'POST':
        print("POST request received")
        print(f"POST data: {request.POST}")
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            print(f"Form data - Name: {name}, Email: {email}, Subject: {subject}")
            
            # Validate required fields
            if not all([name, email, subject, message]):
                missing_fields = []
                if not name: missing_fields.append('name')
                if not email: missing_fields.append('email')
                if not subject: missing_fields.append('subject')
                if not message: missing_fields.append('message')
                
                error_msg = f'Missing required fields: {", ".join(missing_fields)}'
                print(f"Validation error: {error_msg}")
                messages.error(request, error_msg)
                return render(request, 'contact.html')
            
            full_message = f"""
            Name: {name}
            Email: {email}
            Message: {message}
            """
            print("Attempting to send email...")
            
            # Send email with better error handling
            try:
                send_mail(
                    subject=f"{subject} (From {name})",
                    message=full_message,
                    from_email=settings.EMAIL_HOST_USER,  # Use configured sender
                    recipient_list=[settings.EMAIL_HOST_USER],  # Send to yourself
                    fail_silently=False,
                )
                print("Email sent successfully!")
                messages.success(request, 'Your message was sent successfully!')
                return redirect('home')
                
            except Exception as email_error:
                print(f"Email sending failed: {str(email_error)}")
                messages.error(request, f'Failed to send email: {str(email_error)}')
                return render(request, 'contact.html')
            
        except Exception as e:
            print(f"General error in contact view: {str(e)}")
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'contact.html')
    
    # GET request
    print("Rendering contact form (GET request)")
    return render(request, 'contact.html')

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