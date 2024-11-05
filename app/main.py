from fastapi import FastAPI   
from .core.exceptions import register_error_handlers
from .api import router

version = "v1"

app = FastAPI(
    title="Online Course Platform", 
    description="An Online Marketplace API that allows users to find, buy, and handle courses.", 
    version=version,
    debug=True
)

app.include_router(router=router)

register_error_handlers(app)

@app.get("/")
def home():
    return "Welcome home!"