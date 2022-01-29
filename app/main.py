from database import db

connection = db.connect()

db.create_tables(connection)