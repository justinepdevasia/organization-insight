from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(index=True)
    email: str 
    created_at: datetime

