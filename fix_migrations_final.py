"""
Финальный скрипт для исправления миграций.
Использование: python fix_migrations_final.py
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telehub.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

def fix_migrations():
    """Исправляет проблему с миграциями"""
    with connection.cursor() as cursor:
        # Полностью очищаем таблицу миграций
        cursor.execute("DELETE FROM django_migrations")
        print("Таблица миграций очищена")
        
        recorder = MigrationRecorder(connection)
        
        # Помечаем миграции в правильном порядке (с учетом зависимостей)
        # Сначала базовые миграции Django
        migrations_order = [
            ('contenttypes', '0001_initial'),
            ('contenttypes', '0002_remove_content_type_name'),
            ('auth', '0001_initial'),
            ('auth', '0002_alter_permission_name_max_length'),
            ('auth', '0003_alter_user_email_max_length'),
            ('auth', '0004_alter_user_username_opts'),
            ('auth', '0005_alter_user_last_login_null'),
            ('auth', '0006_require_contenttypes_0002'),
            ('auth', '0007_alter_validators_add_error_messages'),
            ('auth', '0008_alter_user_username_max_length'),
            ('auth', '0009_alter_user_last_name_max_length'),
            ('auth', '0010_alter_group_name_max_length'),
            ('auth', '0011_update_proxy_permissions'),
            ('auth', '0012_alter_user_first_name_max_length'),
            # Теперь cards (зависит от auth)
            ('cards', '0001_initial'),
            # Затем admin (зависит от auth и contenttypes)
            ('admin', '0001_initial'),
            ('admin', '0002_logentry_remove_auto_add'),
            ('admin', '0003_logentry_add_action_flag_choices'),
            # Sessions
            ('sessions', '0001_initial'),
        ]
        
        applied_count = 0
        for app, name in migrations_order:
            try:
                recorder.record_applied(app, name)
                applied_count += 1
            except Exception as e:
                print(f"Ошибка при пометке {app}.{name}: {e}")
        
        print(f"Помечено {applied_count} миграций")
        print("\nТеперь выполните: python manage.py migrate")

if __name__ == '__main__':
    try:
        fix_migrations()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        print("\nАльтернативное решение:")
        print("1. Остановите сервер Django (Ctrl+C)")
        print("2. Удалите файл db.sqlite3")
        print("3. Выполните: python manage.py migrate")

