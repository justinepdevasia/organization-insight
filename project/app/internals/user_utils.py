from sqlmodel import select
from sqlmodel import Session
from fastapi import HTTPException

from app.internals.user_utils import *
from app.models.users import Users

def get_users(session: Session):
    query = select(Users)
    users = session.exec(query).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users
