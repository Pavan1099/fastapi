from fastapi import FastAPI
import models
from database import engine
from routers import products
from config import get_settings

# Load settings
settings = get_settings()

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG_MODE)

# Include Routers
app.include_router(products.router)


@app.get("/")
def greet():
    """
    Root endpoint to verify API availability.
    """
    return {"message": f"Welcome to {settings.APP_NAME}", "docs_url": "/docs"}
