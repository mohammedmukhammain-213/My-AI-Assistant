import sqlite3


DATABASE = "database/memory.db"


# ==================================================
# INITIALIZE DATABASE
# ==================================================

def init_database():

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==================================================
# SAVE MESSAGE
# ==================================================

def save_message(role, content):

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        """
        INSERT INTO messages (role, content)
        VALUES (?, ?)
        """,
        (role, content)
    )

    conn.commit()
    conn.close()


# ==================================================
# GET RECENT MESSAGES
# ==================================================

def get_messages(limit=10):

    conn = sqlite3.connect(DATABASE)

    rows = conn.execute(
        """
        SELECT role, content
        FROM messages
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    conn.close()

    return list(reversed(rows))


# ==================================================
# SAVE FACT
# ==================================================

def save_fact(key, value):

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        """
        INSERT INTO facts (key, value)
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
        """,
        (key, value)
    )

    conn.commit()
    conn.close()


# ==================================================
# GET FACTS
# ==================================================

def get_facts():

    conn = sqlite3.connect(DATABASE)

    rows = conn.execute(
        """
        SELECT key, value
        FROM facts
        ORDER BY id ASC
        """
    ).fetchall()

    conn.close()

    unique_facts = {}

    for key, value in rows:
        unique_facts[key] = value

    return list(unique_facts.items())


# ==================================================
# DELETE FACT
# ==================================================

def delete_fact(key):

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        """
        DELETE FROM facts
        WHERE key = ?
        """,
        (key,)
    )

    conn.commit()
    conn.close()


# ==================================================
# DELETE ALL FACTS
# ==================================================

def delete_all_facts():

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        """
        DELETE FROM facts
        """
    )

    conn.commit()
    conn.close()
