"""
Скрипт для исправления проблемы с миграциями.
Использование: python fix_migrations.py
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telehub.settings')
django.setup()

from django.db import connection

def fix_migrations():
    """Исправляет проблему с миграциями"""
    with connection.cursor() as cursor:
        # Полностью очищаем таблицу миграций
        cursor.execute("DELETE FROM django_migrations")
        
        # Помечаем миграции как примененные в правильном порядке
        from django.db.migrations.recorder import MigrationRecorder
        
        recorder = MigrationRecorder(connection)
        
        # ВАЖНО: cards должна быть первой, так как от неё зависят другие
        migrations_to_fake = [
            ('cards', '0001_initial'),  # Сначала cards!
            ('contenttypes', '0001_initial'),
            ('auth', '0001_initial'),
            ('admin', '0001_initial'),
            ('sessions', '0001_initial'),
            ('messages', '0001_initial'),
        ]
        
        for app, name in migrations_to_fake:
            try:
                recorder.record_applied(app, name)
                print(f"OK: Помечена миграция {app}.{name}")
            except Exception as e:
                print(f"ERROR: Ошибка при пометке {app}.{name}: {e}")
        
        print("Миграции очищены и базовые миграции помечены как примененные.")
        print("Теперь выполните: python manage.py migrate --fake-initial")
        print("Или удалите db.sqlite3 и выполните: python manage.py migrate")

if __name__ == '__main__':
    try:
        fix_migrations()
    except Exception as e:
        print(f"Ошибка: {e}")
        print("\nАльтернативное решение:")
        print("1. Остановите сервер Django (Ctrl+C)")
        print("2. Удалите файл db.sqlite3 вручную")
        print("3. Выполните: python manage.py migrate")

