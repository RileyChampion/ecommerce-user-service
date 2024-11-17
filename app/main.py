from fastapi import FastAPI
from app.api.v1 import api_router
# from app.db.session import engine, Base
# from app.config import settings

app = FastAPI(title="EComm User Service")

app.include_router(api_router, prefix="/api/v1")

# Base.metadata.create_all(bind=engine)
