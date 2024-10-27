from fastapi import FastAPI  
from app.database.main import engine, Base
from app.core.errors import register_error_handlers

version = "v1"

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Course Platform", 
    description="An Online Marketplace API that allows users to find, buy, and handle courses.", 
    version=version
)

register_error_handlers(app)

@app.get("/")
def home():
    return "Welcome home!"


