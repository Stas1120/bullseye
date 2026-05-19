import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
"""
def test_add_existing_user(setup_database):
    add_user('stas', 'gmail@gmail.com', 'password123')
    result = add_user('stas', 'mail@gmail.com', 'password456')
    assert result is False
"""""
Тест успешной аутентификации пользователя.
"""""
def test_authenticate_existing_user_success(setup_database):
    add_user('asan', 'asan@mail.ru', 'password111')
    result = authenticate_user('asan', 'password111')
    assert result is True
"""""
Тест аутентификации несуществующего пользователя.
"""""
def test_authenticate_nonexistent_user(setup_database):
    result = authenticate_user('ares', 'password8')
    assert result is False
"""""
Тест аутентификации пользователя с неправильным паролем.
"""""
def test_authenticate_user_wrong_password(setup_database):
    add_user('yarik', 'yarik@gmail.com', 'password')
    result = authenticate_user('yarik', 'wrongpassword')
    assert result is False
"""""
Тест отображения списка пользователей.
"""
def test_authenticate_user(setup_database):
    add_user('taras', 'taras@mail.ru', 'drowssap')
    result = authenticate_user('taras', 'drowssap')
    assert result is True