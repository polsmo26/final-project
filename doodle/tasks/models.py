from django.db import models
from accounts.models import User
from django.utils import timezone

class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    description = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # due_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True, verbose_name="Due Date")
    
    @property
    def is_past_due(self):
        if self.due_date:
            return timezone.now().date() > self.due_date
        return False
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-due_date']