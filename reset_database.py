"""
Скрипт для полной пересборки базы данных.
ИСПОЛЬЗОВАНИЕ: Остановите сервер Django, затем выполните: python reset_database.py
"""
import os
import sys

# Проверка, что сервер не запущен
try:
    import sqlite3
    db_path = 'db.sqlite3'
    
    if os.path.exists(db_path):
        # Пытаемся открыть базу данных в режиме эксклюзивного доступа
        try:
            conn = sqlite3.connect(db_path)
            conn.execute('PRAGMA journal_mode=WAL')
            conn.close()
            
            # Удаляем базу данных
            os.remove(db_path)
            print("✓ База данных db.sqlite3 удалена")
        except PermissionError:
            print("✗ ОШИБКА: База данных заблокирована!")
            print("  Пожалуйста, остановите сервер Django (Ctrl+C) и попробуйте снова.")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Ошибка: {e}")
            sys.exit(1)
    else:
        print("✓ База данных не существует, создадим новую")
    
    print("\nТеперь выполните следующие команды:")
    print("1. python manage.py migrate")
    print("2. python manage.py createsuperuser")
    print("3. python manage.py runserver")
    
except Exception as e:
    print(f"Ошибка: {e}")
    print("\nАльтернативное решение:")
    print("1. Остановите сервер Django (Ctrl+C)")
    print("2. Вручную удалите файл db.sqlite3")
    print("3. Выполните: python manage.py migrate")

