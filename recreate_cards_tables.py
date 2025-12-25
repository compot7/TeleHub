"""
Скрипт для пересоздания таблиц cards.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telehub.settings')
django.setup()

from django.db import connection

def recreate_tables():
    """Удаляет запись о миграции и пересоздает таблицы"""
    with connection.cursor() as cursor:
        # Удаляем запись о миграции cards
        cursor.execute("DELETE FROM django_migrations WHERE app = 'cards'")
        print("Запись о миграции cards удалена")
        
        # Проверяем, какие таблицы cards должны существовать
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'cards_%'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        if existing_tables:
            print(f"Найдены существующие таблицы cards: {existing_tables}")
            print("Удаляю их...")
            for table in existing_tables:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table}")
                    print(f"  Удалена таблица: {table}")
                except Exception as e:
                    print(f"  Ошибка при удалении {table}: {e}")
        
        print("\nТеперь выполните: python manage.py migrate cards")

if __name__ == '__main__':
    try:
        recreate_tables()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

