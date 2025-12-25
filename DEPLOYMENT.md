# Инструкции по развертыванию

## Production настройки

### 1. Обновление settings.py

Для production необходимо обновить следующие настройки в `telehub/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-secret-key-here'  # Сгенерируйте новый ключ

# База данных PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'telehub_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Безопасность
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Сбор статических файлов

```bash
python manage.py collectstatic --noinput
```

### 3. Настройка веб-сервера (Nginx + Gunicorn)

#### Установка Gunicorn

```bash
pip install gunicorn
```

#### Запуск через Gunicorn

```bash
gunicorn telehub.wsgi:application --bind 0.0.0.0:8000
```

#### Пример конфигурации Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/TeleHub/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/TeleHub/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Настройка Google Maps API

1. Получите API ключ на https://console.cloud.google.com/
2. Откройте `templates/cards/card_detail.html`
3. Найдите строку с `YOUR_API_KEY` и замените на ваш ключ

### 5. Настройка медиа-файлов

Для production рекомендуется использовать облачное хранилище (AWS S3, Google Cloud Storage и т.д.) или настроить отдельный сервер для медиа-файлов.

### 6. Резервное копирование

Настройте регулярное резервное копирование базы данных:

```bash
python manage.py dumpdata > backup.json
```

### 7. Мониторинг

Рекомендуется настроить мониторинг ошибок (Sentry, Rollbar) и логирование.

## Безопасность

- Используйте HTTPS
- Регулярно обновляйте зависимости
- Настройте файрвол
- Используйте сильные пароли
- Ограничьте доступ к административной панели

