from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, Query
from app.internals.user_utils import *
from app.db import get_session
from app.models.companies import CompanyResponse, IposResponse, AcquisitionResponse, AcquiredResponse
from sqlmodel import Session


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Users])
async def get_all_users(
    session: Session = Depends(get_session)
):
    users = get_users(session)
    return users