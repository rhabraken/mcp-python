import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration using environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# SQL statements to create tables
TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now()
        );
    """,
    "organisations": """
        CREATE TABLE IF NOT EXISTS organisations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now()
        );
    """,
    "organisation_access": """
        CREATE TABLE IF NOT EXISTS organisation_access (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            organisation_id UUID REFERENCES organisations(id) ON DELETE CASCADE,
            role TEXT CHECK (role IN ('admin', 'member', 'viewer')) NOT NULL,
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now(),
            UNIQUE (user_id, organisation_id)
        );
    """,
    "chats": """
        CREATE TABLE IF NOT EXISTS chats (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organisation_id UUID REFERENCES organisations(id) ON DELETE CASCADE,
            user_id UUID REFERENCES users(id) ON DELETE SET NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now()
        );
    """,
    "conversations": """
        CREATE TABLE IF NOT EXISTS conversations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            chat_id UUID REFERENCES chats(id) ON DELETE CASCADE,
            user_id UUID REFERENCES users(id) ON DELETE SET NULL,
            content JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT now()
        );
    """,
    "account_integrations": """
        CREATE TABLE IF NOT EXISTS account_integrations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organisation_id UUID REFERENCES organisations(id) ON DELETE CASCADE,
            provider TEXT NOT NULL,
            credentials JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now(),
            UNIQUE (organisation_id, provider)
        );
    """
}

def create_tables():
    """Connects to the PostgreSQL database and creates the necessary tables."""
    try:
        # Establish the database connection
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # Execute each table creation query
        for table_name, table_sql in TABLES.items():
            print(f"Creating table: {table_name}")
            cursor.execute(table_sql)

        # Commit the transactions
        connection.commit()
        print("Tables created successfully.")

    except Exception as e:
        print(f"Error creating tables: {e}")

    finally:
        # Close the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    create_tables()
