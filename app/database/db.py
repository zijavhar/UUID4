import sqlite3

# Table create 
CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT, password TEXT);"
CREATE_ACCESS_TABLE = "CREATE TABLE IF NOT EXISTS access (id INTEGER PRIMARY KEY, name TEXT, description TEXT);"
CREATE_FILE_TABLE = """CREATE TABLE IF NOT EXISTS file 
    (id INTEGER PRIMARY KEY, 
    name TEXT, 
    access_id INTEGER,
    user_id INTEGER,
    number_of_downloads INTEGER NOT NULL,
    FOREIGN KEY(access_id) REFERENCES access(id),
    FOREIGN KEY(user_id) REFERENCES user(id));"""

# Tables insert
INSERT_USER = "INSERT INTO user (name, password) VALUES (?, ?);"

# Connect to DB
def connect():
    return sqlite3.connect("database/uuid4.db")

def create_tables(connection):
    with connection:
        # access table
        connection.execute(CREATE_ACCESS_TABLE)
        # user table
        connection.execute(CREATE_USER_TABLE)
        # file table
        connection.execute(CREATE_FILE_TABLE)

def add_user(connection, name: str, password: str):
    with connection:
        connection.execute(INSERT_USER, (name, password))