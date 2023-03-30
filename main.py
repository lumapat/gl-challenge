from fastapi import FastAPI
import sqlite3

app = FastAPI()

# set up SQLite database connection
conn = sqlite3.connect('/app/mydatabase.db', check_same_thread=False)
print('Database connection established.')

# create a users table
conn.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL);''')
conn.commit()
print('Users table created.')

# define routes
@app.get("/")
def index():
    return {"message": "Welcome to my REST API!"}

@app.get("/users")
def get_users():
    cursor = conn.execute('SELECT * FROM users;')
    users = [{'id': row[0], 'name': row[1], 'email': row[2], 'password': row[3]} for row in cursor.fetchall()]
    return {'users': users}
