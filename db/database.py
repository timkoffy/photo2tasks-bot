import sqlite3
import uuid

DB_PATH = "../sessions.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_uuid TEXT UNIQUE NOT NULL,
                chat_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                creator_username TEXT,
                creator_name TEXT,
                title TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            );
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                item_number INTEGER,
                item_type TEXT,
                title TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS selections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
            );
        """)

def create_session(chat_id: int, message_id: int, creator_username: str, creator_name: str, title: str) -> str:
    session_uuid = str(uuid.uuid4())
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO sessions (session_uuid, chat_id, message_id, creator_username, creator_name, title)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (session_uuid, chat_id, message_id, creator_username, creator_name, title)
        )
    return session_uuid

def delete_session(session_uuid: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM sessions WHERE session_uuid = ?", (session_uuid,))