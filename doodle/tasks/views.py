from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.views.decorators.http import require_POST
from datetime import datetime
from datetime import timedelta
import calendar
from django.utils.safestring import mark_safe

def task_calendar(request):
    # First, check if user has ANY tasks with due dates
    user_has_due_dates = Task.objects.filter(
        user=request.user,
        due_date__isnull=False
    ).exists()
    
    # If no tasks have due dates, show message instead of calendar
    if not user_has_due_dates:
        context = {
            'no_due_dates': True,
        }
        return render(request, 'tasks/task_calendar.html', context)
    
    
    # Get year/month from URL (default: current month)
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    
    # Calculate previous and next month
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1])
    
    prev_month = (first_day - timedelta(days=1)).strftime("%Y-%m")
    next_month = (last_day + timedelta(days=1)).strftime("%Y-%m")
    
    # Get all days in month
    cal = calendar.monthcalendar(year, month)
    
    # Get tasks for this month and organize by day
    tasks = Task.objects.filter(
        user=request.user,
        due_date__isnull = False,
        due_date__year=year,
        due_date__month=month
    ).order_by('due_date')
    
    # Create a dictionary of tasks by day
    tasks_by_day = {}
    for task in tasks:
        if task.due_date:
            day = task.due_date.day
            if day not in tasks_by_day:
                tasks_by_day[day] = []
            tasks_by_day[day].append(task)
    
    # Prepare previous/next month navigation
    prev_month_year, prev_month_month = prev_month.split('-')
    next_month_year, next_month_month = next_month.split('-')

    context = {
        'year': year,
        'month': month,
        'month_name': first_day.strftime("%B"),
        'weeks': cal,
        'tasks_by_day': tasks_by_day,
        'prev_month_year': prev_month_year,
        'prev_month_month': prev_month_month,
        'next_month_year': next_month_year,
        'next_month_month': next_month_month,
    }
    return render(request, 'tasks/task_calendar.html', context)

@login_required
def index(request):
    status = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user)
    # Status Filter
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)
    # Difficulty Filter
    difficulty = request.GET.get('difficulty')
    if difficulty in ['E', 'M', 'H']:
        tasks = tasks.filter(difficulty=difficulty)
    # Sorting
    sort = request.GET.get('sort', 'title')  # Default sort by title
    valid_sorts = ['title', '-title', 'difficulty', '-difficulty']
    if sort in valid_sorts:
        tasks = tasks.order_by(sort)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_create.html', {'form': form})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form':form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('tasks:task_list')

@require_POST
@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('tasks:task_list')
