import json
import psycopg2

#логин:
#soy
#пароль:
#your_password


# Читаем параметры подключения из файла
with  open("config.json", "r") as f:
    data = json.load(f)
    host = data["database"]['host']
    port = data["database"]['port']
    database = data["database"]['database']
    user = input("Введите логин пользователя: ")
    password = input("Введите пароль пользователя: ")

# Подключение к базе данных
connection = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Выполнение SQL-запроса
with connection.cursor() as cursor:
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"Версия PostgreSQL: {version}")

# Закрываем соединение
connection.close()
