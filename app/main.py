from .database import db
from fastapi import FastAPI
from .routers import auth

# bootstrap
connection = db.connect()
db.create_tables(connection)
db.seed(connection)

app = FastAPI()

app.include_router(auth.router)

