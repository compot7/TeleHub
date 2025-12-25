from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Публичные страницы
    path('', views.home, name='home'),
    path('card/<str:username>/', views.card_detail, name='card_detail'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('dashboard/login/', auth_views.LoginView.as_view(template_name='cards/login.html'), name='login'),
    path('dashboard/logout/', views.logout_view, name='logout'),
    
    # Личный кабинет
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile_edit, name='profile_edit'),
    
    # Портфолио
    path('dashboard/portfolio/', views.portfolio_list, name='portfolio_list'),
    path('dashboard/portfolio/add/', views.portfolio_add, name='portfolio_add'),
    path('dashboard/portfolio/<int:pk>/edit/', views.portfolio_edit, name='portfolio_edit'),
    path('dashboard/portfolio/<int:pk>/delete/', views.portfolio_delete, name='portfolio_delete'),
    
    # Отзывы (только просмотр и удаление своих отзывов)
    path('dashboard/testimonials/', views.testimonials_list, name='testimonials_list'),
    path('dashboard/testimonials/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),
    
]

