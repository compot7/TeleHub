"""
Скрипт для проверки и исправления таблиц в базе данных.
"""
import os
import sys
import django
import sqlite3

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telehub.settings')
django.setup()

from django.db import connection

def check_tables():
    """Проверяет наличие таблиц"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        return tables

def fix_tables():
    """Проверяет и исправляет таблицы"""
    tables = check_tables()
    print(f"Найдено таблиц: {len(tables)}")
    print(f"Таблицы: {', '.join(tables)}")
    
    required_table = 'cards_customuser'
    if required_table not in tables:
        print(f"\nОШИБКА: Таблица {required_table} не найдена!")
        print("Миграции помечены как примененные, но таблицы не созданы.")
        print("\nРешение:")
        print("1. Удалите запись о миграции cards.0001_initial")
        print("2. Примените миграцию заново")
        print("\nВыполняю исправление...")
        
        with connection.cursor() as cursor:
            # Удаляем запись о миграции cards
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cards'")
            print("OK: Запись о миграции cards удалена")
        
        print("\nТеперь выполните: python manage.py migrate")
        return False
    else:
        print(f"\n✓ Таблица {required_table} существует")
        return True

if __name__ == '__main__':
    try:
        if not fix_tables():
            sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

