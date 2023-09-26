from .database import engine
from . import models
from .routers import post, users, auth, vote
from fastapi import FastAPI


## NOT needed anymore because of alembic migration
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    """
    API root

    Returns:
        str: JSON con un mensaje
    """
    return {"message": "Welcome to my API"}
