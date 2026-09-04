from fastapi import FastAPI
from auth import validate_api_key_configuration
from database import create_tables
from routes import books, users


app = FastAPI(
    title="Kitab Exchange API",
    description="A simple API for exchanging used books",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    validate_api_key_configuration()
    create_tables()

app.include_router(users.router)
app.include_router(books.router)



@app.get("/")
def home():
    return {"message": "Welcome to the Kitab Exchange API"} 
