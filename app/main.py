from fastapi.middleware.cors import CORSMiddleware
from .routers import post, users, auth, vote
from fastapi import FastAPI


# NOT needed anymore because of alembic migration
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, 
                   allow_origins=origins,
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

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
