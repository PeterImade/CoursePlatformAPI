from fastapi import FastAPI  
from .database.main import initDB
from .core.errors import register_error_handlers
from .routers import router

version = "v1"

app = FastAPI(
    title="Online Course Platform", 
    description="An Online Marketplace API that allows users to find, buy, and handle courses.", 
    version=version
)

app.include_router(router=router)

register_error_handlers(app)

@app.get("/")
def home():
    return "Welcome home!"