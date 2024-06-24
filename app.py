import os
import psycopg2


import os
import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )
    cur = conn.cursor()
    cur.execute("""CREATE TABLE Authors (
        Id SERIAL PRIMARY KEY,
        Name VARCHAR(255) NOT NULL
    );

    CREATE TABLE Publishers (
        Id SERIAL PRIMARY KEY,
        Name VARCHAR(255) NOT NULL
    );

    CREATE TABLE Books (
        Id SERIAL PRIMARY KEY,
        Title VARCHAR(255) NOT NULL,
        AuthorId INT REFERENCES Authors(Id),
        PublisherId INT REFERENCES Publishers(Id),
        Price DECIMAL(10, 2) NOT NULL
    );

    CREATE TABLE Orders (
        Id SERIAL PRIMARY KEY,
        BookId INT REFERENCES Books(Id),
        Quantity INT NOT NULL,
        OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    INSERT INTO Authors (Name) VALUES ('Author 1'), ('Author 2');
    INSERT INTO Publishers (Name) VALUES ('Publisher 1'), ('Publisher 2');
    INSERT INTO Books (Title, AuthorId, PublisherId, Price) VALUES
    ('Book 1', 1, 1, 19.99),
    ('Book 2', 2, 2, 29.99);
    INSERT INTO Orders (BookId, Quantity) VALUES (1, 2), (2, 1);


    CREATE USER books_user_1 WITH PASSWORD 'password123';
    GRANT CONNECT, TEMPORARY ON DATABASE books_db TO books_user_1;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO books_user_1;""")
    return conn

def list_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        for table in tables:
            print(table[0])

def view_table(conn, table, filter_column=None, filter_value=None):
    query = f"SELECT * FROM {table}"
    if filter_column and filter_value:
        query += f" WHERE {filter_column} = %s"
    with conn.cursor() as cur:
        cur.execute(query, (filter_value,))
        rows = cur.fetchall()
        for row in rows:
            print(row)

def update_record(conn, table, id, new_data):
    set_clause = ", ".join(f"{column} = %({column})s" for column in new_data.keys())
    with conn.cursor() as cur:
        cur.execute(f"""
            UPDATE {table} SET {set_clause} WHERE Id = %s
        """, {**new_data, 'Id': id})
        conn.commit()

def insert_record(conn, table, data):
    columns = ', '.join(data.keys())
    values = ', '.join(f'%({keys}' for key in data.keys())
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO {table} ({columns}) VALUES ({values})
        """, data)
        conn.commit()

def main():
    conn = connect_to_db()
    while True:
        print("\n1. List tables")
        print("2. View table")
        print("3. Update record")
        print("4. Insert record")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            list_tables(conn)
        elif choice == '2':
            table = input("Enter table name: ")
            filter_column = input("Enter filter column (leave blank for no filter): ")
            filter_value = input("Enter filter value (leave blank for no filter): ")
            view_table(conn, table, filter_column, filter_value)
        elif choice == '3':
            table = input("Enter table name: ")
            id = input("Enter record ID: ")
            data = {}
            for key in input("Enter column names and new values separated by space: ").split():
                if '=' in key:
                    column, value = key.split('=')
                    data[column] = value
            update_record(conn, table, id, data)
        elif choice == '4':
            table = input("Enter table name: ")
            data = {}
            for key in input("Enter column names and values separated by space: ").split():
                if '=' in key:
                    column, value = key.split('=')
                    data[column] = value
            insert_record(conn, table, data)
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

    conn.close()


if __name__ == "__main__":
    main()