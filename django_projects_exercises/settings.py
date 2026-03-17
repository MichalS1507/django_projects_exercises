"""
Django settings for django_projects_exercises project.

This module contains all configuration settings for the Django project,
including database configuration, installed apps, middleware, templates,
and security settings. It uses environment variables for sensitive data.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This keeps sensitive data like SECRET_KEY out of version control
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the root directory of the project (where manage.py lives)
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# Loaded from environment variable - NEVER commit this to version control
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode provides detailed error pages - should be False in production
# Value is read from environment variable, defaults to False if not set
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hosts/domain names that this Django site can serve
# In production, add your domain here (e.g., ['example.com', 'www.example.com'])
ALLOWED_HOSTS = []

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

# List of Django apps that are enabled in this project
# Order matters for template loading and migrations
INSTALLED_APPS = [
    # Custom apps
    'todo_app',  # Main todo_app application

    'properties',

    'rest_framework',
    'corsheaders',

    # Django built-in apps
    'django.contrib.admin',  # Admin interface
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content type system (for permissions)
    'django.contrib.sessions',  # Session management
    'django.contrib.messages',  # Flash messages
    'django.contrib.staticfiles',  # Static file management
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Middleware components - process requests and responses globally
# Order is important - each middleware wraps the next
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Associate users with requests
    'django.contrib.messages.middleware.MessageMiddleware',  # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Root URL configuration - points to the main urls.py
ROOT_URLCONF = 'django_projects_exercises.urls'

# Template engine configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Directories where Django looks for templates (besides app directories)
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # Whether to look for templates inside app directories
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Makes request object available in templates
                'django.template.context_processors.request',
                # Makes user authentication data available
                'django.contrib.auth.context_processors.auth',
                # Makes flash messages available
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path for deployment
WSGI_APPLICATION = 'django_projects_exercises.wsgi.application'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Database configuration
# Using SQLite for development - easy to set up and no external dependencies
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

# Password validation rules for user authentication
# These help ensure users choose secure passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Prevents passwords too similar to user attributes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Enforces minimum password length (default: 8 characters)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Prevents commonly used weak passwords
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Prevents passwords that are entirely numeric
    },
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

# Default language for the project
LANGUAGE_CODE = 'en-us'

# Time zone for date/time display
# Set to Central European Time for Slovakia/Czech Republic
TIME_ZONE = 'Europe/Bratislava'

# Enable Django's translation system
USE_I18N = True

# Enable timezone-aware datetime handling
# When True, Django uses timezone-aware datetimes
USE_TZ = True

# =============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# =============================================================================

# URL prefix for static files
STATIC_URL = 'static/'

# =============================================================================
# AUTHENTICATION SETTINGS
# =============================================================================

# URL where login page is located
# Used by LoginRequiredMixin to redirect unauthenticated users
LOGIN_URL = '/accounts/login/'

# Where to redirect after successful login
# Sends users to the main task list page
LOGIN_REDIRECT_URL = '/todo/'

# Where to redirect after logout
# Also sends users to the main task list (login required will redirect back)
LOGOUT_REDIRECT_URL = '/todo/'