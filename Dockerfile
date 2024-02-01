# Используем образ PostgreSQL 16
FROM postgres:16

# Устанавливаем необходимые локали
RUN localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8

# Переопределяем переменные окружения для PostgreSQL
ENV LANG ru_RU.utf8