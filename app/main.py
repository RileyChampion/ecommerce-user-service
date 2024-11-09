from fastapi import FastAPI
from app.api.v1 import routes
from app.db.session import engine, Base
from app.config import settings

app = FastAPI(title= "User Service")

app.include_router(routes.router, prefix="/api/v1")

Base.metadata.create_all(bind=engine)