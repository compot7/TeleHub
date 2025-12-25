"""
Скрипт для создания таблиц cards напрямую через SQL.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telehub.settings')
django.setup()

from django.db import connection

# SQL из миграции cards.0001_initial
SQL = """
BEGIN;
CREATE TABLE IF NOT EXISTS "cards_customuser" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "avatar" varchar(100) NULL, "background_image" varchar(100) NULL, "title" varchar(200) NOT NULL, "bio" text NOT NULL, "skills" varchar(500) NOT NULL, "phone" varchar(20) NOT NULL, "email_public" varchar(254) NOT NULL, "address" varchar(300) NOT NULL, "location_lat" decimal NULL, "location_lng" decimal NULL, "accent_color" varchar(7) NOT NULL, "theme" varchar(10) NOT NULL);
CREATE TABLE IF NOT EXISTS "cards_customuser_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "customuser_id" bigint NOT NULL REFERENCES "cards_customuser" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "cards_customuser_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "customuser_id" bigint NOT NULL REFERENCES "cards_customuser" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "cards_testimonial" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "text" text NOT NULL, "author_name" varchar(100) NOT NULL, "author_position" varchar(200) NOT NULL, "author_photo" varchar(100) NULL, "is_published" bool NOT NULL, "created_at" datetime NOT NULL, "order" integer NOT NULL, "user_id" bigint NOT NULL REFERENCES "cards_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "cards_sociallink" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "platform" varchar(20) NOT NULL, "url" varchar(200) NOT NULL, "icon" varchar(50) NOT NULL, "user_id" bigint NOT NULL REFERENCES "cards_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "cards_portfolioitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "description" text NOT NULL, "category" varchar(100) NOT NULL, "image" varchar(100) NOT NULL, "images" text NOT NULL, "project_url" varchar(200) NOT NULL, "github_url" varchar(200) NOT NULL, "date" date NULL, "order" integer NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "cards_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "cards_contactmessage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(20) NOT NULL, "message" text NOT NULL, "is_read" bool NOT NULL, "created_at" datetime NOT NULL, "card_user_id" bigint NOT NULL REFERENCES "cards_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX IF NOT EXISTS "cards_customuser_groups_customuser_id_group_id_6cb17b7d_uniq" ON "cards_customuser_groups" ("customuser_id", "group_id");
CREATE INDEX IF NOT EXISTS "cards_customuser_groups_customuser_id_21ca4168" ON "cards_customuser_groups" ("customuser_id");
CREATE INDEX IF NOT EXISTS "cards_customuser_groups_group_id_cb41cb61" ON "cards_customuser_groups" ("group_id");
CREATE UNIQUE INDEX IF NOT EXISTS "cards_customuser_user_permissions_customuser_id_permission_id_65c95168_uniq" ON "cards_customuser_user_permissions" ("customuser_id", "permission_id");
CREATE INDEX IF NOT EXISTS "cards_customuser_user_permissions_customuser_id_a9026c95" ON "cards_customuser_user_permissions" ("customuser_id");
CREATE INDEX IF NOT EXISTS "cards_customuser_user_permissions_permission_id_aa8fe4ae" ON "cards_customuser_user_permissions" ("permission_id");
CREATE INDEX IF NOT EXISTS "cards_testimonial_user_id_8d5ed3f5" ON "cards_testimonial" ("user_id");
CREATE INDEX IF NOT EXISTS "cards_sociallink_user_id_abc0214d" ON "cards_sociallink" ("user_id");
CREATE INDEX IF NOT EXISTS "cards_portfolioitem_user_id_dddb9b11" ON "cards_portfolioitem" ("user_id");
CREATE INDEX IF NOT EXISTS "cards_contactmessage_card_user_id_414d2bd2" ON "cards_contactmessage" ("card_user_id");
COMMIT;
"""

def create_tables():
    """Создает таблицы cards"""
    try:
        with connection.cursor() as cursor:
            # Выполняем SQL по частям (SQLite не поддерживает множественные команды в execute)
            commands = [cmd.strip() for cmd in SQL.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
            
            for cmd in commands:
                if cmd and cmd.upper() not in ['BEGIN', 'COMMIT']:
                    try:
                        cursor.execute(cmd)
                        print(f"OK: {cmd[:50]}...")
                    except Exception as e:
                        # Игнорируем ошибки "table already exists"
                        if 'already exists' not in str(e).lower():
                            print(f"Ошибка при выполнении {cmd[:50]}: {e}")
            
            connection.commit()
            print("\nТаблицы cards успешно созданы!")
            return True
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_tables()

