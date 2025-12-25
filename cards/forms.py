from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, PortfolioItem, Testimonial


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя с улучшенной валидацией пароля"""
    email = forms.EmailField(
        required=True, 
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        help_text='Обязательно. 150 символов или меньше. Только буквы, цифры и @/./+/-/_'
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        help_text='''
        <ul class="password-requirements">
            <li>Минимум 8 символов</li>
            <li>Должен содержать хотя бы одну заглавную букву</li>
            <li>Должен содержать хотя бы одну строчную букву</li>
            <li>Должен содержать хотя бы одну цифру</li>
            <li>Не должен быть слишком похож на другую личную информацию</li>
            <li>Не должен быть слишком простым (например, "password123")</li>
        </ul>
        '''
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        help_text='Введите тот же пароль для подтверждения'
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                validate_password(password1, self.instance)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError({
                'password2': 'Пароли не совпадают'
            })
        
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""
    class Meta:
        model = CustomUser
        fields = ['avatar', 'background_image', 'title', 'bio', 'skills', 
                 'phone', 'email_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Веб-разработчик'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Расскажите о себе...'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Навыки через запятую'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'email_public': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class PortfolioItemForm(forms.ModelForm):
    """Форма для проекта портфолио"""
    class Meta:
        model = PortfolioItem
        fields = ['title', 'description', 'category', 'image', 'archive', 'date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'date': forms.DateInput(attrs={'type': 'date', 'required': True}),
        }


class TestimonialForm(forms.ModelForm):
    """Форма для отзыва на визитке другого пользователя"""
    class Meta:
        model = Testimonial
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш отзыв...'}),
        }



