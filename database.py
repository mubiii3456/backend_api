import os
import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    
    conn = psycopg.connect(DATABASE_URL)
    return conn

def init_db():
   
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        );
    """)

    
    cur.execute("SELECT COUNT(*) FROM tasks;")
    count = cur.fetchone()[0]

    
    if count == 0:
        cur.execute("""
            INSERT INTO tasks (title, done) VALUES 
            ('Learn Docker', true),
            ('Connect Postgres to Python', false),
            ('Complete Stage 1', false);
        """)

    conn.commit()
    cur.close()
    conn.close()