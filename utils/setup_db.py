from os import getenv
import sqlite3

db_path = getenv("DB_PATH", "/app/mydatabase.db")

setup_query = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
"""

if __name__ == "__main__":
    conn = sqlite3.connect(db_path)
    print('Database connection established!')

    conn.execute(setup_query)
    conn.commit()
    print('Tables created!')