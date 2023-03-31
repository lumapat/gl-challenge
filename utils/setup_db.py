from os import getenv
import sqlite3

db_path = getenv("DB_PATH", "/app/mydatabase.db")

# TODO: Put these into files to run in sequence
setup_queries = [
    """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS loan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loan_term INTEGER NOT NULL,
        amount NUMERIC(38, 10) NOT NULL,
        annual_ir NUMERIC(5, 4) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS loan_user (
        user_id INTEGER NOT NULL,
        loan_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, loan_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (loan_id) REFERENCES loans(id)
    );
    """
]

if __name__ == "__main__":
    conn = sqlite3.connect(db_path)
    print('Database connection established!')

    for q in setup_queries:
        conn.execute(q)
    conn.commit()
    print('Tables created!')