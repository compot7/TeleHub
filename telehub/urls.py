"""
URL configuration for telehub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cards.urls')),
]

# Раздача медиа-файлов (нужно для Render, так как нет отдельного веб-сервера)
# В продакшене рекомендуется использовать облачное хранилище (S3, Cloudinary и т.д.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Раздача статических файлов только в DEBUG режиме (в продакшене используется WhiteNoise)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

