import sqlite3
import uuid
from typing import List, Dict, Any, Optional

DB_PATH = "sessions.db"

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
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                item_number INTEGER,
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
                selected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
                UNIQUE(item_id, user_id)
            );
        """)

# session managing
def create_session(chat_id: int, message_id: int, creator_username: str, creator_name: str, title: str) -> tuple:
    session_uuid = str(uuid.uuid4())
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """INSERT INTO sessions (session_uuid, chat_id, message_id, creator_username, creator_name, title)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (session_uuid, chat_id, message_id, creator_username, creator_name, title)
        )
        session_id = cursor.lastrowid
    return session_uuid, session_id

def delete_session(session_uuid: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM sessions WHERE session_uuid = ?", (session_uuid,))

def get_session_by_uuid(session_uuid: str) -> Optional[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM sessions WHERE session_uuid = ?", (session_uuid,)).fetchone()
        return dict(row) if row else None

def get_session_by_message_id(chat_id: int, message_id: int) -> Optional[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM sessions WHERE chat_id = ? AND message_id = ?",
            (chat_id, message_id)
        ).fetchone()
        return dict(row) if row else None

def get_session_by_id(session_id: int) -> Optional[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        return dict(row) if row else None

def delete_expired_sessions(days: int = 1):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM sessions WHERE created_at < datetime('now', ?)",
            (f"-{days} days",)
        )


# item managing
def add_item(session_id: int, item_number: int, title: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO items (session_id, item_number, title)
               VALUES (?, ?, ?)""",
            (session_id, item_number, title)
        )

def get_items_by_session(session_id: int) -> List[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM items WHERE session_id = ? ORDER BY item_number",
            (session_id,)
        ).fetchall()
        return [dict(row) for row in rows]


# select item methods
def select_item(item_id: int, user_id: int, username: str, first_name: str, last_name: str) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """INSERT INTO selections (item_id, user_id, username, first_name, last_name)
                   VALUES (?, ?, ?, ?, ?)""",
                (item_id, user_id, username, first_name, last_name)
            )
        return True
    except sqlite3.IntegrityError:
        return False

def unselect_item(item_id: int, user_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "DELETE FROM selections WHERE item_id = ? AND user_id = ?",
            (item_id, user_id)
        )
        return cursor.rowcount > 0

def get_selections_for_item(item_id: int) -> List[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM selections WHERE item_id = ?",
            (item_id,)
        ).fetchall()
        return [dict(row) for row in rows]

def clear_user_selections(session_id: int, user_id: int) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            DELETE FROM selections
            WHERE item_id IN (SELECT id FROM items WHERE session_id = ?)
            AND user_id = ?
        """, (session_id, user_id))
        return cursor.rowcount