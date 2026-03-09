from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Task, Category


class TaskModelTest(TestCase):
    """Test suite for the Task model."""

    def setUp(self):
        """Create test data before each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            color='#ff0000'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            priority=1,
            category=self.category,
            user=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )

    def test_task_creation(self):
        """Verify task is created with correct attributes."""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.priority, 1)
        self.assertEqual(self.task.category, self.category)
        self.assertEqual(self.task.user, self.user)
        self.assertFalse(self.task.completed)

    def test_task_str_method(self):
        """Verify string representation includes title and priority."""
        expected = "Test Task (High)"
        self.assertEqual(str(self.task), expected)

    def test_is_overdue_property(self):
        """Verify overdue detection works correctly."""
        # Task should not be overdue (deadline in future)
        self.assertFalse(self.task.is_overdue)

        # Set deadline to yesterday
        self.task.due_date = timezone.now() - timedelta(days=1)
        self.task.save()
        self.assertTrue(self.task.is_overdue)

    def test_mark_completed(self):
        """Verify task can be marked as completed."""
        self.task.mark_completed()
        self.assertTrue(self.task.completed)

    def test_mark_incomplete(self):
        """Verify completed task can be marked as incomplete."""
        self.task.completed = True
        self.task.save()
        self.task.mark_incomplete()
        self.assertFalse(self.task.completed)

    def test_priority_color_property(self):
        """Verify correct color codes are returned for each priority level."""
        # High priority (1) should return red
        self.task.priority = 1
        self.task.save()
        self.task.refresh_from_db()
        self.assertEqual(self.task.priority_color, '#dc3545')

        # Medium priority (2) should return yellow
        self.task.priority = 2
        self.task.save()
        self.task.refresh_from_db()
        self.assertEqual(self.task.priority_color, '#ffc107')

        # Low priority (3) should return green
        self.task.priority = 3
        self.task.save()
        self.task.refresh_from_db()
        self.assertEqual(self.task.priority_color, '#28a745')

    def test_clean_method_past_due_date(self):
        """Verify validation prevents due dates in the past."""
        from django.core.exceptions import ValidationError

        self.task.due_date = timezone.now() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.task.clean()


class CategoryModelTest(TestCase):
    """Test suite for the Category model."""

    def setUp(self):
        """Create test category before each test method."""
        self.category = Category.objects.create(
            name='Work',
            color='#007bff'
        )

    def test_category_creation(self):
        """Verify category is created with correct attributes."""
        self.assertEqual(self.category.name, 'Work')
        self.assertEqual(self.category.color, '#007bff')

    def test_category_str_method(self):
        """Verify string representation returns category name."""
        self.assertEqual(str(self.category), 'Work')


class TaskListViewTest(TestCase):
    """Test suite for TaskListView."""

    def setUp(self):
        """Set up test user, login, and create sample tasks."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

        # Create tasks with different states for filter testing
        self.task1 = Task.objects.create(
            title='Task 1',
            priority=1,
            user=self.user,
            completed=False
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            priority=2,
            user=self.user,
            completed=True
        )
        self.task3 = Task.objects.create(
            title='Task 3',
            priority=3,
            user=self.user,
            completed=False
        )

    def test_list_view_url(self):
        """Verify list view responds at correct URL."""
        response = self.client.get('/todo/')
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """Verify correct template is used."""
        response = self.client.get(reverse('todo_app:task_list'))
        self.assertTemplateUsed(response, 'todo_app/task_index.html')

    def test_list_view_context(self):
        """Verify context contains tasks."""
        response = self.client.get(reverse('todo_app:task_list'))
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 3)

    def test_filter_all(self):
        """Verify 'all' filter returns all tasks."""
        response = self.client.get(reverse('todo_app:task_list') + '?filter=all')
        self.assertEqual(len(response.context['tasks']), 3)

    def test_filter_completed(self):
        """Verify 'completed' filter returns only completed tasks."""
        response = self.client.get(reverse('todo_app:task_list') + '?filter=completed')
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertTrue(response.context['tasks'][0].completed)

    def test_filter_incomplete(self):
        """Verify 'incomplete' filter returns only pending tasks."""
        response = self.client.get(reverse('todo_app:task_list') + '?filter=incomplete')
        self.assertEqual(len(response.context['tasks']), 2)
        self.assertFalse(response.context['tasks'][0].completed)


class TaskDetailViewTest(TestCase):
    """Test suite for TaskDetailView."""

    def setUp(self):
        """Create users and a test task."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=self.user
        )

    def test_detail_view_url(self):
        """Verify detail view responds at correct URL."""
        response = self.client.get(f'/todo/{self.task.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Verify correct template is used."""
        response = self.client.get(
            reverse('todo_app:task_detail', args=[self.task.pk])
        )
        self.assertTemplateUsed(response, 'todo_app/task_detail.html')

    def test_detail_view_context(self):
        """Verify context contains the task."""
        response = self.client.get(
            reverse('todo_app:task_detail', args=[self.task.pk])
        )
        self.assertEqual(response.context['task'], self.task)

    def test_other_user_cannot_view_task(self):
        """Verify users cannot access tasks belonging to others."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('todo_app:task_detail', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 404)


class TaskCreateViewTest(TestCase):
    """Test suite for TaskCreateView."""

    def setUp(self):
        """Set up authenticated user and a category."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Test', color='#ff0000')

    def test_create_view_url(self):
        """Verify create view responds at correct URL."""
        response = self.client.get(reverse('todo_app:new_task'))
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Verify correct template is used."""
        response = self.client.get(reverse('todo_app:new_task'))
        self.assertTemplateUsed(response, 'todo_app/task_form.html')

    def test_create_task_post(self):
        """Verify task creation via POST request."""
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 2,
            'category': self.category.pk,
            'due_date': timezone.now() + timedelta(days=1),
        }
        response = self.client.post(reverse('todo_app:new_task'), data)

        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)

        # Verify task was created with correct attributes
        task = Task.objects.get(title='New Task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.priority, 2)


class TaskUpdateViewTest(TestCase):
    """Test suite for TaskUpdateView."""

    def setUp(self):
        """Set up authenticated user and a test task."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            title='Old Title',
            description='Old Description',
            user=self.user
        )

    def test_update_view_url(self):
        """Verify update view responds at correct URL."""
        response = self.client.get(
            reverse('todo_app:update_task', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_update_task_post(self):
        """Verify task update via POST request."""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'priority': 3,
        }
        response = self.client.post(
            reverse('todo_app:update_task', args=[self.task.pk]),
            data
        )

        self.assertEqual(response.status_code, 302)

        # Verify task was updated
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertEqual(self.task.description, 'Updated Description')


class TaskDeleteViewTest(TestCase):
    """Test suite for TaskDeleteView."""

    def setUp(self):
        """Set up authenticated user and a task to delete."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            title='Task to delete',
            user=self.user
        )

    def test_delete_view_get(self):
        """Verify GET request shows confirmation modal."""
        response = self.client.get(
            reverse('todo_app:delete_task', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/task_detail.html')
        self.assertTrue(response.context['delete_mode'])

    def test_delete_view_post(self):
        """Verify POST request deletes the task."""
        response = self.client.post(
            reverse('todo_app:delete_task', args=[self.task.pk])
        )

        self.assertEqual(response.status_code, 302)

        # Verify task no longer exists
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task.pk)


class TaskCompleteViewTest(TestCase):
    """Test suite for TaskCompleteView."""

    def setUp(self):
        """Set up authenticated user and an incomplete task."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            title='Task to complete',
            user=self.user,
            completed=False
        )

    def test_complete_task_post(self):
        """Verify task can be marked as completed via POST."""
        response = self.client.post(
            reverse('todo_app:complete_task', args=[self.task.pk])
        )

        self.assertEqual(response.status_code, 302)

        # Verify task is now completed
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)


class AuthenticationTest(TestCase):
    """Test suite for authentication requirements."""

    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_required_for_tasks(self):
        """Verify unauthenticated users are redirected to login."""
        response = self.client.get(reverse('todo_app:task_list'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_login_view(self):
        """Verify user can log in successfully."""
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login