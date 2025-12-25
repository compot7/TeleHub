from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, PortfolioItem, Testimonial, ContactMessage


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Административная панель для пользователей"""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Профиль визитки', {
            'fields': ('avatar', 'background_image', 'title', 'bio', 'skills', 
                      'phone', 'email_public', 'address', 'location_lat', 'location_lng',
                      'accent_color', 'theme')
        }),
    )
    list_display = ['username', 'email', 'title', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'theme']


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'date', 'created_at']
    list_filter = ['category', 'date']
    search_fields = ['title', 'user__username']
    ordering = ['-created_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'user', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['author_name', 'user__username']
    ordering = ['order', '-created_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'card_user', 'email', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'card_user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

