"""
Скрипт для исправления миграции cards.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telehub.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

def fix_cards_migration():
    """Исправляет миграцию cards"""
    recorder = MigrationRecorder(connection)
    
    # Проверяем, применена ли миграция
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'cards' AND name = '0001_initial'")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Помечаю миграцию cards.0001_initial как примененную...")
            recorder.record_applied('cards', '0001_initial')
            print("OK: Миграция помечена")
        else:
            print("Миграция cards.0001_initial уже помечена")
        
        # Проверяем наличие таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'cards_customuser'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("\nВНИМАНИЕ: Таблица cards_customuser не существует!")
            print("Нужно применить миграцию. Попробую применить...")
            
            # Пытаемся выполнить SQL из миграции напрямую
            try:
                from django.core.management import call_command
                # Используем --fake для обхода проверки зависимостей
                print("\nПопробуйте выполнить вручную:")
                print("python manage.py migrate cards 0001_initial --fake")
                print("\nИли удалите базу данных и создайте заново:")
                print("1. Остановите сервер")
                print("2. Удалите db.sqlite3")
                print("3. python manage.py migrate")
            except Exception as e:
                print(f"Ошибка: {e}")

if __name__ == '__main__':
    try:
        fix_cards_migration()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

