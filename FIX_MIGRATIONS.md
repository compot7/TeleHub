# Исправление ошибки миграций

## Проблема
Ошибка: `no such table: cards_customuser` или `InconsistentMigrationHistory`

Эта ошибка возникает, когда база данных была создана до настройки кастомной модели пользователя.

## Решение: Удаление и пересоздание базы данных (РЕКОМЕНДУЕТСЯ)

### Шаг 1: Остановите сервер Django
**ОБЯЗАТЕЛЬНО!** Нажмите `Ctrl+C` в терминале, где запущен сервер Django.

### Шаг 2: Удалите базу данных

**Вариант A: Используйте скрипт (проще)**
```bash
python reset_database.py
```

**Вариант B: Вручную через PowerShell**
```powershell
Remove-Item db.sqlite3 -Force
```

**Вариант C: Вручную через проводник Windows**
- Откройте папку проекта
- Найдите файл `db.sqlite3`
- Удалите его

### Шаг 3: Примените миграции
```bash
python manage.py migrate
```

### Шаг 4: Создайте суперпользователя
```bash
python manage.py createsuperuser
```

### Шаг 5: Запустите сервер
```bash
python manage.py runserver
```

Готово! Ошибка должна быть исправлена.

## Решение 2: Использование скрипта исправления

1. Остановите сервер Django

2. Запустите скрипт исправления:
   ```bash
   python fix_migrations.py
   ```

3. Примените миграции:
   ```bash
   python manage.py migrate
   ```

## Решение 3: Ручное исправление через SQL

Если база данных не заблокирована:

1. Откройте базу данных:
   ```bash
   python manage.py dbshell
   ```

2. Выполните SQL команды:
   ```sql
   DELETE FROM django_migrations WHERE app = 'admin';
   DELETE FROM django_migrations WHERE app = 'auth';
   DELETE FROM django_migrations WHERE app = 'contenttypes';
   ```

3. Выйдите из dbshell (Ctrl+D или .quit)

4. Примените миграции:
   ```bash
   python manage.py migrate
   ```

## Причина проблемы

Проблема возникает, когда база данных была создана до того, как была настроена кастомная модель пользователя `CustomUser`. Django пытается применить миграции в неправильном порядке.

После исправления все должно работать корректно!

