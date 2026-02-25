from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    """
    Model representing a task category.
    Each category has a name and a color for visual identification.
    """
    name = models.CharField(max_length=50)  # Category name (e.g., Work, Personal)
    color = models.CharField(max_length=7, default='#007bff')   # Hex color code for UI

    def __str__(self):
        # String representation of the category (returns its name).
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Task(models.Model):
    """
    Model representing a task in the todo application.
    Each task belongs to a user and optionally to a category.
    """
    # Priority choices for the task
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    # Basic task information
    title = models.CharField(max_length=200)    # Task title/short description
    description = models.TextField(blank=True)  # Detailed description (optional)

    # Date fields
    created_date = models.DateTimeField(auto_now_add=True)  # Auto-set when task is created
    due_date = models.DateTimeField(null=True, blank=True)  # Deadline (optional)

    # Status fields
    completed = models.BooleanField(default=False)  # Task completion status
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES,
                                default='L')    # Task priority (Low, Medium, High)

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 blank=True)    # Optional category, set to NULL if category is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # Task owner, deleted if user is deleted

    def __str__(self):
        # String representation showing title and priority.
        return f"{self.title} ({self.get_priority_display()})"

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['completed', 'priority', 'due_date']    # Default ordering: incomplete first, then by priority, then by date

    @property
    def is_overdue(self):
        """
        Check if the task is overdue.
        Returns True if due_date exists, task is not completed, and due_date is in the past.
        """
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False

    def mark_completed(self):
        # Mark the task as completed and save to database.
        self.completed = True
        self.save()

    def mark_incomplete(self):
        # Mark the task as incomplete and save to database.
        self.completed = False
        self.save()

    @property
    def priority_color(self):
        """
        Return CSS color code based on task priority.
        Used for visual styling in templates.
        """
        colors = {'H': '#dc3545',   # Red for High priority
                  'M': '#ffc107',   # Yellow for Medium priority
                  'L': '#28a745'    # Green for Low priority
        }
        return colors.get(self.priority, '#6c757d') # Default gray if priority not found

    def clean(self):
        """
        Custom validation for the task model.
        Ensures due_date cannot be in the past.
        """
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError({'due_date': 'Due date cannot be in the past!'})