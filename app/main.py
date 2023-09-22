from .database import engine
from . import models
from .routers import post, users, auth
from fastapi import FastAPI
from .config import Settings



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    """
    API root

    Returns:
        str: JSON con un mensaje
    """
    return {"message": "Welcome to my API"}
