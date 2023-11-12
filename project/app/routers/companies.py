from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, Query
from app.internals.user_utils import *
from app.db import get_session
from app.models.companies import CompanyResponse, IposResponse, AcquisitionResponse, AcquiredResponse
from sqlmodel import Session


router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    offset: int = 0, 
    limit: int = Query(default=100, le=100),
    company_name: str = Query(None, description="Filter by company name"),
    country_code: str = Query(None, description="Filter by country code"),
    acquisitions: bool = Query(None, description="Filter by companies with acquisitions"),
    acquired: bool = Query(None, description="Filter by companies that have been acquired"),
    session: Session = Depends(get_session)
):
    filtered_companies = None

    if company_name:
        filtered_companies = [get_company_by_name(session, company_name)]

    if country_code:
        filtered_companies = get_companies_by_country_code(session, country_code, offset, limit)

    if acquisitions is not None:
        filtered_companies = get_companies_with_acquisitions(session, offset, limit)

    if acquired is not None:
        filtered_companies = get_acquired_companies(session, offset, limit)
    
    if not filtered_companies:
        filtered_companies = get_all_companies(session, offset, limit)

    return filtered_companies

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: Annotated[str, Path(title="The ID of the item to get")],
    session: Session = Depends(get_session)
):
    company_info = get_company_info(session, company_id)
    return company_info

@router.get("/{company_id}/ipo_info", response_model=List[IposResponse])
async def get_ipo_info(
    company_id: Annotated[str, Path(title="The ID of the item to get")],
    session: Session = Depends(get_session)
):
    ipo_info = get_company_ipo_info(session, company_id)
    return ipo_info

@router.get("/{company_id}/acquired_info", response_model=List[AcquiredResponse])
async def get_acquired(
    company_id: Annotated[str, Path(title="The ID of the item to get")],
    session: Session = Depends(get_session)
):
    acquired_info = get_acquired_info(session, company_id)
    return acquired_info

@router.get("/{company_id}/acquisition_info", response_model=List[AcquisitionResponse])
async def get_acquisition(
    company_id: Annotated[str, Path(title="The ID of the item to get")],
    session: Session = Depends(get_session)
):
    acquisition_info = get_acquisition_info(session, company_id)
    return acquisition_info
