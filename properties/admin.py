from django.contrib import admin
from .models import Property, PropertyImage, Booking

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'city', 'offer_type', 'is_available']
    list_filter = ['offer_type', 'property_type', 'city', 'is_available']
    search_fields = ['title', 'description', 'address']
    inlines = [PropertyImageInline]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_main']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'created_at']
    list_filter = ['created_at']
