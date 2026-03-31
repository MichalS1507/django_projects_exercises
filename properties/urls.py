from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegisterView

router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet)
router.register(r'images', views.PropertyImageViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
