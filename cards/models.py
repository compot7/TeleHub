from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    """Расширенная модель пользователя для хранения данных профиля"""
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, verbose_name='Фоновое изображение')
    title = models.CharField(max_length=200, blank=True, verbose_name='Должность')
    bio = models.TextField(blank=True, verbose_name='Биография')
    skills = models.CharField(max_length=500, blank=True, help_text='Навыки через запятую', verbose_name='Навыки')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email_public = models.EmailField(blank=True, verbose_name='Публичный email')
    address = models.CharField(max_length=300, blank=True, verbose_name='Адрес')
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Широта')
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Долгота')
    accent_color = models.CharField(max_length=7, default='#007bff', verbose_name='Акцентный цвет')
    theme = models.CharField(max_length=10, choices=[('light', 'Светлая'), ('dark', 'Темная')], default='light', verbose_name='Тема')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'username': self.username})


class SocialLink(models.Model):
    """Модель для хранения социальных ссылок пользователя"""
    SOCIAL_CHOICES = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('vk', 'VKontakte'),
        ('website', 'Веб-сайт'),
        ('other', 'Другое'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='social_links', verbose_name='Пользователь')
    platform = models.CharField(max_length=20, choices=SOCIAL_CHOICES, verbose_name='Платформа')
    url = models.URLField(verbose_name='URL')
    icon = models.CharField(max_length=50, blank=True, help_text='Класс иконки (Font Awesome)', verbose_name='Иконка')
    
    class Meta:
        verbose_name = 'Социальная ссылка'
        verbose_name_plural = 'Социальные ссылки'
        ordering = ['platform']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_platform_display()}"


class PortfolioItem(models.Model):
    """Модель проекта портфолио"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolio_items', verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=100, blank=True, verbose_name='Категория')
    image = models.ImageField(upload_to='portfolio/', verbose_name='Изображение')
    images = models.JSONField(default=list, blank=True, help_text='Дополнительные изображения (JSON массив)', verbose_name='Дополнительные изображения')
    archive = models.FileField(upload_to='portfolio/archives/', blank=True, null=True, verbose_name='Архив проекта')
    date = models.DateField(verbose_name='Дата проекта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Проект портфолио'
        verbose_name_plural = 'Проекты портфолио'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Testimonial(models.Model):
    """Модель отзыва"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='testimonials', verbose_name='Владелец визитки')
    author_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authored_testimonials', verbose_name='Автор отзыва', null=True, blank=True)
    text = models.TextField(verbose_name='Текст отзыва')
    author_name = models.CharField(max_length=100, verbose_name='Имя автора')
    author_position = models.CharField(max_length=200, blank=True, verbose_name='Должность автора')
    author_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name='Фото автора')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.author_name}"


class ContactMessage(models.Model):
    """Модель сообщения из формы обратной связи"""
    card_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contact_messages', verbose_name='Владелец визитки')
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} -> {self.card_user.username}"

