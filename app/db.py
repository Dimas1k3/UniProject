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

    conn.commit()
    conn.close()

def get_tasks_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, is_done, created_at, completed_at
        FROM tasks
    ''')    

    tasks = cursor.fetchall()
    task_lst = []

    for task in tasks:
        task_id = task[0]
        title = task[1]
        
        if task[2] == 0:
            done_status = False
        else:
            done_status = True

        task_lst.append({
            "id": task_id,
            "title": title,
            "done": done_status
        })

    conn.close()
    # print(task_lst)
    return task_lst

def add_task_to_db(task):
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_done = 0
    title = task

    cursor.execute('''
        INSERT INTO tasks (title, is_done, created_at)
        VALUES (?, ?, ?)
    ''', (title, is_done, created_at))

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }

def delete_task_from_db(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM tasks WHERE id = ?
    ''', (task_id,)) 

    conn.commit()
    conn.close()

def update_task_status(task_id, task_status):
    conn = get_connection()
    cursor = conn.cursor()

    if task_status == True:
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            UPDATE tasks 
            SET is_done = ?, completed_at = ? 
            WHERE id = ?
        ''', (1, completed_at, task_id))
    else:
        cursor.execute('''
            UPDATE tasks 
            SET is_done = ?, completed_at = NULL 
            WHERE id = ?
        ''', (0, task_id))

    conn.commit()
    conn.close()

# ---------------------------------------------

def get_sites_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, url, is_active, created_at, last_blocked, total_blocks
        FROM sites
    ''')

    sites = cursor.fetchall()
    site_lst = []

    for site in sites:
        site_id = site[0]
        url = site[1]
        
        if site[2] == 0:
            active_status = False
        else:
            active_status = True

        site_lst.append({
            "id": site_id,
            "url": url,
            "is_active": active_status
        })

    conn.close()
    return site_lst

def add_site_to_db(url):
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_active = 0

    cursor.execute('''
        INSERT INTO sites (url, is_active, created_at)
        VALUES (?, ?, ?)
    ''', (url, is_active, created_at))

    conn.commit()
    site_id = cursor.lastrowid
    conn.close()

    return {
        "id": site_id,
        "url": url,
        "is_active": False
    }

def delete_site_from_db(site_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM sites WHERE id = ?
    ''', (site_id,)) 

    conn.commit()
    conn.close()

def update_site_status(site_id, is_active):
    conn = get_connection()
    cursor = conn.cursor()

    if is_active == True:
        cursor.execute('SELECT total_blocks FROM sites WHERE id = ?', (site_id,))
        result = cursor.fetchone()
        
        if not result:
            total_blocks = 0
        else:
            total_blocks = result[0]

        total_blocks += 1

        last_blocked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            UPDATE sites 
            SET is_active = ?, last_blocked = ?, total_blocks = ?
            WHERE id = ?
        ''', (1, last_blocked, total_blocks, site_id))

    else:
        cursor.execute('''
            UPDATE sites 
            SET is_active = ?
            WHERE id = ?
        ''', (0, site_id))

    conn.commit()
    conn.close()
