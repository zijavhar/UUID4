from .database import db
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import auth, file

# bootstrap
connection = db.connect()
db.create_tables(connection)
db.seed(connection)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(file.router)

