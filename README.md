# Django TODO Application

A full-featured task management application built with Django. This project demonstrates CRUD operations, user authentication, task filtering, and comprehensive testing.

## Features

- User Authentication - Secure login/logout system with password protection
- Task Management - Create, read, update, and delete tasks
- Categories - Organize tasks with color-coded categories
- Priority Levels - High/Medium/Low priority with visual indicators
- Due Dates - Set deadlines with automatic overdue detection
- Filtering - Filter tasks by status (All/Active/Completed)
- Responsive Design - Works on desktop and mobile devices
- Security - Each user sees only their own tasks

## Technologies Used

- Backend: Django 4.2, Python 3.12
- Database: SQLite
- Frontend: HTML5, CSS3 (custom CSS, no frameworks)
- Testing: Django TestCase (29 tests)
- Version Control: Git

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository
   ```
   git clone https://github.com/MichalS1507/django_projects_exercises.git
   cd django_projects_exercises
   ```

2. Create and activate virtual environment
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. Run database migrations
   ```
   python manage.py migrate
   ```

6. Create a superuser (admin)
   ```
   python manage.py createsuperuser
   ```

7. Start the development server
   ```
   python manage.py runserver
   ```

8. Access the application
   - Main app: http://127.0.0.1:8000/todo/
   - Admin interface: http://127.0.0.1:8000/admin/

## Testing

The application includes 29 comprehensive tests covering models, views, and authentication.

Run the tests with:
```
python manage.py test todo_app
```

Test coverage includes:
- Task model methods and properties
- Category model functionality
- View responses and templates
- Filtering logic
- User authentication
- Security (users cannot access others' tasks)

## Project Structure

```
django_projects_exercises/
├── todo_app/                    # Main application
│   ├── migrations/              # Database migrations
│   ├── templates/               # HTML templates
│   │   ├── registration/        # Login template
│   │   └── todo_app/            # App-specific templates
│   ├── static/                   # CSS files
│   ├── admin.py                  # Admin configuration
│   ├── forms.py                   # Form definitions
│   ├── models.py                  # Database models
│   ├── tests.py                   # Test suite
│   ├── urls.py                    # URL routing
│   └── views.py                   # Business logic
├── django_projects_exercises/    # Project settings
├── .env                          # Environment variables (not in repo)
├── .gitignore                    # Git ignore rules
├── manage.py                      # Django management script
└── requirements.txt               # Python dependencies
```

## Key Learning Points

- Django Architecture - MVT pattern, URL routing, class-based views
- Database Design - Models, relationships, migrations
- User Authentication - LoginRequiredMixin, user-specific data filtering
- Testing - Unit tests, test-driven development concepts
- Security - CSRF protection, password hashing, data isolation
- Frontend - Responsive design, custom CSS, template inheritance
- Version Control - Git workflow, meaningful commits

## Contact

Michal Šmatlák - michal.smatlak@gmail.com

GitHub: MichalS1507

---

Note: This application was developed as part of my learning journey in Django. It demonstrates my ability to build, test, and document a complete web application.