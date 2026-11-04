
import os

import psycopg
from dotenv import load_dotenv

# Load database settings from the .env file
load_dotenv()

# Connect to the Sentinel PostgreSQL database
def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )



# Test the database connection
if __name__ == "__main__":
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database();")
                result = cursor.fetchone()
                print("Connected to database:", result[0])

    except Exception as error:
        print("Database connection failed:", error)
