from fastapi import FastAPI
import sqlite3

app = FastAPI()

# set up SQLite database connection
conn = sqlite3.connect('/app/mydatabase.db', check_same_thread=False)
print('Database connection established.')

# define routes
@app.get("/")
def index():
    return {"message": "Welcome to my REST API!"}

@app.get("/users")
def get_users():
    cursor = conn.execute('SELECT * FROM users;')
    users = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    return {'users': users}
