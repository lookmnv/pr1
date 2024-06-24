import os
import psycopg2
import time
import sys
import logging

def get_db_version():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host='db'
        )
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            version = cur.fetchone()
            logging.info(f"DB Version: {version[0]}")
        conn.close()
    except Exception as e:
        logging.error(f"Error connecting to DB: {e}")

if __name__ == "__main__":
    interval = int(os.getenv('CHECK_INTERVAL', '300'))  # Default to 5 minutes
    log_file = os.getenv('LOG_FILE')

    if log_file:
        logging.basicConfig(filename=log_file, filemode='a', level=logging.INFO)

    while True:
        get_db_version()
        time.sleep(interval)