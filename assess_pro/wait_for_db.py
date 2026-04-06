import time
import psycopg2

while True:
    try:
        conn = psycopg2.connect(
            dbname="rates_db",
            user="postgres",
            password="postgres",
            host="db",
            port=5432,
        )
        print("Database is ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for database...")
        time.sleep(2)