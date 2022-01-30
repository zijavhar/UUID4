import sqlite3
from ..utils import hash
# Table create 
CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT UNIQUE, password TEXT);"
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
INSERT_FILE = "INSERT INTO file (name, access_id, user_id, number_of_downloads) VALUES (?, ?, ?, ?);"
# Tables select
GET_USER_BY_NAME = "SELECT * FROM user WHERE name = (?)"
GET_FILES_FOR_SPECIFIC_USER = "SELECT * FROM file WHERE user_id = (?) OR access_id = 1 ORDER BY number_of_downloads DESC"
# Connect to DB
def connect():
    return sqlite3.connect("app/database/uuid4.db")

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

def get_user_by_name(connection, name: str):
    with connection:
        return connection.execute(GET_USER_BY_NAME, (name,)).fetchone()

def seed(connection):
    with connection:
        # check whether rows exist
        count = connection.execute("SELECT COUNT(*) FROM access").fetchone()
        if count[0] == 0:
            connection.execute("""INSERT INTO access (id, name, description) 	
                VALUES (1, 'all', 'Доступен всем'),
	            (2, 'link', 'Доступен только по ссылке'),
	            (3, 'private', 'Доступен только мне');""")
        count = connection.execute("SELECT COUNT(*) FROM user WHERE name='admin'").fetchone()
        if count[0] == 0:
            connection.execute("""INSERT INTO user (id, name, password) VALUES (1, 'admin', (?))""", (hash("admin"),))

def create_file(connection, name, access_id, user_id):
    with connection:
        connection.execute(INSERT_FILE, (name, access_id, user_id, 0))

def get_files(connection, user_id):
    with connection:
        return connection.execute(GET_FILES_FOR_SPECIFIC_USER, (user_id,)).fetchall()