import psycopg2
from faker import Faker
import uuid
import json
from datetime import datetime
import random
import os
from dotenv import load_dotenv

load_dotenv()


# Database connection configuration using environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Initialize Faker
fake = Faker()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

# Insert fake data
def insert_fake_data():
    # Insert Users
    user_ids = []
    for _ in range(20):
        user_id = str(uuid.uuid4())
        email = fake.unique.email()
        name = fake.name()
        password_hash = fake.sha256()
        created_at = updated_at = datetime.now()

        cur.execute("""
            INSERT INTO users (id, email, name, password_hash, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, email, name, password_hash, created_at, updated_at))
        user_ids.append(user_id)

    # Insert Organisations
    organisation_ids = []
    for _ in range(5):
        organisation_id = str(uuid.uuid4())
        name = fake.company()
        created_at = updated_at = datetime.now()

        cur.execute("""
            INSERT INTO organisations (id, name, created_at, updated_at)
            VALUES (%s, %s, %s, %s)
        """, (organisation_id, name, created_at, updated_at))
        organisation_ids.append(organisation_id)

    # Insert Organisation Access
    roles = ['admin', 'member', 'viewer']
    for user_id in user_ids:
        for organisation_id in random.sample(organisation_ids, k=2):
            access_id = str(uuid.uuid4())
            role = random.choice(roles)
            created_at = updated_at = datetime.now()

            cur.execute("""
                INSERT INTO organisation_access (id, user_id, organisation_id, role, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (access_id, user_id, organisation_id, role, created_at, updated_at))

    # Insert Chats
    chat_ids = []
    for organisation_id in organisation_ids:
        for _ in range(3):
            chat_id = str(uuid.uuid4())
            user_id = random.choice(user_ids)
            title = fake.sentence(nb_words=4)
            created_at = updated_at = datetime.now()

            cur.execute("""
                INSERT INTO chats (id, organisation_id, user_id, title, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (chat_id, organisation_id, user_id, title, created_at, updated_at))
            chat_ids.append(chat_id)

    # Insert Conversations
    for chat_id in chat_ids:
        for _ in range(5):
            conversation_id = str(uuid.uuid4())
            user_id = random.choice(user_ids)
            content = json.dumps({"message": fake.text(max_nb_chars=200)})
            created_at = datetime.now()

            cur.execute("""
                INSERT INTO conversations (id, chat_id, user_id, content, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (conversation_id, chat_id, user_id, content, created_at))

    # Insert Account Integrations
    providers = ['google', 'slack', 'github']
    for organisation_id in organisation_ids:
        for provider in providers:
            integration_id = str(uuid.uuid4())
            credentials = json.dumps({
                "api_key": fake.sha256(),
                "secret": fake.sha256()
            })
            created_at = updated_at = datetime.now()

            cur.execute("""
                INSERT INTO account_integrations (id, organisation_id, provider, credentials, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (integration_id, organisation_id, provider, credentials, created_at, updated_at))

    # Commit the transaction
    conn.commit()
    print("Fake data inserted successfully!")

# Run the data insertion
insert_fake_data()

# Close the connection
cur.close()
conn.close()
