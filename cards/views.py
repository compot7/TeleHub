from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
import json

from .models import CustomUser, PortfolioItem, Testimonial
from .forms import (CustomUserCreationForm, ProfileEditForm, PortfolioItemForm, 
                   TestimonialForm)


def home(request):
    """Главная страница с поиском визиток"""
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(is_active=True)
    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(title__icontains=query) |
            Q(bio__icontains=query)
        )
    
    context = {
        'users': users[:12],  # Показываем первые 12
        'query': query,
    }
    return render(request, 'cards/home.html', context)


def card_detail(request, username):
    """Публичная страница визитки пользователя"""
    card_user = get_object_or_404(CustomUser, username=username, is_active=True)
    portfolio_items = card_user.portfolio_items.all()
    testimonials = card_user.testimonials.filter(is_published=True)
    
    # Обработка навыков
    skills_list = []
    if card_user.skills:
        skills_list = [skill.strip() for skill in card_user.skills.split(',') if skill.strip()][:10]
    
    # Проверяем, может ли текущий пользователь оставить отзыв
    can_leave_testimonial = False
    if request.user.is_authenticated and request.user != card_user:
        can_leave_testimonial = True
    
    # Форма отзыва
    testimonial_form = None
    if can_leave_testimonial:
        if request.method == 'POST' and 'testimonial_submit' in request.POST:
            testimonial_form = TestimonialForm(request.POST, request.FILES)
            if testimonial_form.is_valid():
                testimonial = testimonial_form.save(commit=False)
                testimonial.user = card_user  # Владелец визитки
                testimonial.author_user = request.user  # Автор отзыва
                # Автоматически заполняем данные из профиля пользователя
                testimonial.author_name = request.user.get_full_name() or request.user.username
                testimonial.author_position = request.user.title or ''
                testimonial.author_photo = request.user.avatar
                testimonial.save()
                messages.success(request, 'Отзыв успешно добавлен!')
                return redirect('card_detail', username=username)
        else:
            testimonial_form = TestimonialForm()
    
    context = {
        'card_user': card_user,
        'portfolio_items': portfolio_items,
        'testimonials': testimonials,
        'skills_list': skills_list,
        'can_leave_testimonial': can_leave_testimonial,
        'testimonial_form': testimonial_form,
    }
    return render(request, 'cards/card_detail.html', context)




def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна! Заполните свой профиль.')
            return redirect('profile_edit')  # Перенаправляем в профиль
    else:
        form = CustomUserCreationForm()
    return render(request, 'cards/register.html', {'form': form})


@login_required
def dashboard(request):
    """Главная страница личного кабинета"""
    user = request.user
    portfolio_count = user.portfolio_items.count()
    # Считаем все опубликованные отзывы на визитке пользователя
    testimonials_count = user.testimonials.filter(is_published=True).count()
    
    context = {
        'portfolio_count': portfolio_count,
        'testimonials_count': testimonials_count,
    }
    return render(request, 'cards/dashboard.html', context)


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'cards/profile_edit.html', {'form': form})


@login_required
def portfolio_list(request):
    """Список проектов портфолио"""
    items = request.user.portfolio_items.all()
    return render(request, 'cards/portfolio_list.html', {'items': items})


@login_required
def portfolio_add(request):
    """Добавление проекта портфолио"""
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Проект успешно добавлен!')
            return redirect('portfolio_list')
    else:
        form = PortfolioItemForm()
    
    return render(request, 'cards/portfolio_form.html', {'form': form, 'action': 'Добавить'})


@login_required
def portfolio_edit(request, pk):
    """Редактирование проекта портфолио"""
    item = get_object_or_404(PortfolioItem, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно обновлен!')
            return redirect('portfolio_list')
    else:
        form = PortfolioItemForm(instance=item)
    
    return render(request, 'cards/portfolio_form.html', {'form': form, 'action': 'Редактировать', 'item': item})


@login_required
def portfolio_delete(request, pk):
    """Удаление проекта портфолио"""
    item = get_object_or_404(PortfolioItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Проект удален!')
    return redirect('portfolio_list')


@login_required
def testimonials_list(request):
    """Список отзывов - только те, которые пользователь оставил на других визитках"""
    # Показываем только отзывы, которые текущий пользователь оставил на визитках других людей
    items = request.user.authored_testimonials.all().select_related('user')
    return render(request, 'cards/testimonials_list.html', {'items': items})


@login_required
def testimonial_delete(request, pk):
    """Удаление отзыва - только своих отзывов на других визитках"""
    item = get_object_or_404(Testimonial, pk=pk, author_user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Отзыв удален!')
    return redirect('testimonials_list')


@login_required
def logout_view(request):
    """Выход из системы (принимает GET запросы)"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')





