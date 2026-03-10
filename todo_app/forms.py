"""
Form definitions for the todo_app application.

This module contains form classes that handle data validation and rendering
for task-related operations. It uses Django's ModelForm to automatically
generate forms based on the Task model.
"""
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task instances.

    This form is automatically generated from the Task model and includes
    custom widgets for better user experience. It handles validation
    of all task fields including dates, priorities, and relationships.

    Features:
    - Automatically validates against model constraints
    - Uses datetime-local input for due_date
    - Provides larger text area for descriptions
    - Excludes 'completed' and 'user' fields (handled separately in views)
    """

    class Meta:
        """
        Metadata options for the TaskForm.

        Attributes:
            model: The model class this form is based on
            fields: Tuple of field names to include in the form
            widgets: Dictionary mapping field names to custom widget classes
        """
        model = Task
        # Explicitly list fields to include - 'completed' and 'user' are excluded
        # as they are set automatically in views
        fields = ('title', 'description', 'priority', 'due_date', 'category')

        # Custom widgets for better user interface
        widgets = {
            # datetime-local input provides native browser date/time picker
            'due_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',  # Optional: for consistent styling
                }
            ),
            # Larger text area for multi-line descriptions
            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Enter task description (optional)',
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom behavior.

        This method is called when creating a new form instance.
        It can be used to:
        - Customize field attributes
        - Add additional validation logic
        - Modify querysets for choice fields
        """
        super().__init__(*args, **kwargs)

        # Add common CSS classes to all fields for consistent styling
        for field_name in self.fields:
            # Skip fields that already have custom classes
            if field_name not in ['due_date', 'description']:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control'
                })

        # Customize priority field display
        self.fields['priority'].empty_label = None  # Remove empty choice
        self.fields['priority'].widget.attrs.update({
            'class': 'form-control'
        })

        # Make category field more user-friendly
        self.fields['category'].empty_label = '-- No category --'

        # Add help text for better user guidance
        self.fields['title'].help_text = 'Required: A short, descriptive title'
        self.fields['due_date'].help_text = 'Optional: Set a deadline for this task'
        self.fields['category'].help_text = 'Optional: Assign to a category'

    def clean_title(self):
        """
        Custom validation for the title field.

        Ensures the title has at least 3 characters and is properly formatted.

        Returns:
            str: The cleaned title

        Raises:
            ValidationError: If title is too short or contains invalid characters
        """
        title = self.cleaned_data.get('title')

        if title and len(title.strip()) < 3:
            raise forms.ValidationError(
                'Title must be at least 3 characters long.'
            )

        return title.strip()

    def clean_due_date(self):
        """
        Custom validation for the due_date field.

        While the model's clean() method prevents past dates, this form-level
        validation provides immediate feedback to users.

        Returns:
            datetime: The cleaned due_date
        """
        due_date = self.cleaned_data.get('due_date')

        # Additional form-level validation can be added here
        # Note: Model-level validation already prevents past dates

        return due_date

    def save(self, commit=True):
        """
        Save the form data to create or update a Task instance.

        This method extends the default save behavior to handle
        any additional processing before saving.

        Args:
            commit: Boolean indicating whether to save to database immediately

        Returns:
            Task: The saved task instance
        """
        task = super().save(commit=False)

        # Any pre-save processing can be added here
        # Note: 'user' field is set in the view, not here

        if commit:
            task.save()
            self.save_m2m()  # Save many-to-many relationships if any

        return task