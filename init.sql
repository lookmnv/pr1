-- Создаем базу данных
CREATE DATABASE your_database;

-- Создаем пользователя с доступом USAGE
CREATE USER alex WITH ENCRYPTED PASSWORD 'your_password';
GRANT USAGE ON DATABASE your_database TO alex;

-- Устанавливаем язык для базы данных
ALTER DATABASE your_database SET lc_messages = 'ru_RU.utf8';
