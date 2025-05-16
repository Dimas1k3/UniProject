import sqlite3
from datetime import datetime

DB_PATH = "antiprok.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_done INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            is_active INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            last_blocked TEXT,
            total_blocks INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            is_active INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            last_blocked TEXT,
            total_blocks INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# ------------------------------------------------------------

def get_items_from_db(item_type):
    conn = get_connection()
    cursor = conn.cursor()

    query = {
        "task": "SELECT id, title, is_done FROM tasks",
        "site": "SELECT id, url, is_active FROM sites",
        "app":  "SELECT id, name, is_active FROM apps"
    }[item_type]

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        item = {
            "id": row[0],
            "is_done" if item_type == "task" else "is_active": bool(row[2]),
        }
        if item_type == "task":
            item["title"] = row[1]
        elif item_type == "site":
            item["url"] = row[1]
        else:
            item["name"] = row[1]

        result.append(item)

    return result


def add_item_to_db(item_type, value):
    conn = get_connection()
    cursor = conn.cursor()

    table = {"task": "tasks", "site": "sites", "app": "apps"}[item_type]
    column = {"task": "title", "site": "url", "app": "name"}[item_type]
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "is_done" if table == "tasks" else "is_active"
    
    cursor.execute(f'''
        INSERT INTO {table} ({column}, {status}, created_at)
        VALUES (?, ?, ?)
    ''', (value, 0, created_at))

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return {
        "id": item_id,
        "done" if item_type == "task" else "is_active": False,
        column: value
    }


def delete_item_from_db(item_type, item_id):
    conn = get_connection()
    cursor = conn.cursor()

    table = {"task": "tasks", "site": "sites", "app": "apps"}[item_type]

    cursor.execute(f'''
        DELETE FROM {table} WHERE id = ?
    ''', (item_id,))

    conn.commit()
    conn.close()


def update_item_status(item_type, item_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if item_type == "task":
        if status:
            cursor.execute('''
                UPDATE tasks
                SET is_done = ?, completed_at = ?
                WHERE id = ?
            ''', (1, now, item_id))
        else:
            cursor.execute('''
                UPDATE tasks
                SET is_done = ?, completed_at = NULL
                WHERE id = ?
            ''', (0, item_id))
    else:
        table = {"site": "sites", "app": "apps"}[item_type]

        if status:
            cursor.execute(f'''
                SELECT total_blocks FROM {table} WHERE id = ?
            ''', (item_id,))
            result = cursor.fetchone()
            total_blocks = (result[0] if result else 0) + 1

            cursor.execute(f'''
                UPDATE {table}
                SET is_active = ?, last_blocked = ?, total_blocks = ?
                WHERE id = ?
            ''', (1, now, total_blocks, item_id))
        else:
            cursor.execute(f'''
                UPDATE {table}
                SET is_active = ?
                WHERE id = ?
            ''', (0, item_id))

    conn.commit()
    conn.close()


def reset_status(items, table):
    conn = get_connection()
    cursor = conn.cursor()

    for item in items:
        cursor.execute(
            f"UPDATE {table} SET is_active = ? WHERE id = ?",
            (0, item["id"])
        )

    conn.commit()
    conn.close()


def get_active_apps_from_db():
    conn = sqlite3.connect("antiprok.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM apps WHERE is_active = 1")
    
    result = []
    for row in cursor.fetchall():
        result.append(row[0])
    
    conn.close()
    return result