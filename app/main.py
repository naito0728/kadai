from fastapi import FastAPI
from .database import Base, engine
from .routers import search, logs
from fastapi import FastAPI
from .routers import search, logs, categories, documents, users
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kadai_App")

app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])