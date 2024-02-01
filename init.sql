-- Создаем базу данных
CREATE DATABASE your_database;

-- Создаем пользователя с доступом USAGE
CREATE USER usersoy WITH PASSWORD 'my_pass';
GRANT USAGE ON DATABASE your_database TO usersoy;

-- Устанавливаем язык для базы данных
ALTER DATABASE your_database SET lc_message = 'ru_RU.utf8';

