from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    pass

def create_user(db: Session, user: UserCreate):
    pass