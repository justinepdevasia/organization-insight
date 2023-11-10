from sqlmodel import select
from app.models import Company, Acquisitions
from sqlmodel import Session
from fastapi import HTTPException


def get_company_by_name(session: Session, company_name: str):
    query = select(Company).where(Company.name == company_name)
    company = session.exec(query).one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

def get_companies_by_country_code(session: Session, country_code: str, offset: int, limit: int):
    query = select(Company).where(Company.country_code == country_code.upper()).offset(offset).limit(limit)
    companies = session.exec(query).all()
    if not companies:
        raise HTTPException(status_code=404, detail="Companies with given country code not found")
    return companies

def get_all_companies(session: Session, offset: int, limit: int):
    query = select(Company).offset(offset).limit(limit)
    companies = session.exec(query).all()
    return companies

def get_companies_with_acquisitions(session: Session, offset: int, limit: int):
    # need to query both Company and Acquistion table to get all companies with acquisitions
    query = select(Company).join(
        Acquisitions,
        Company.id == Acquisitions.acquiring_object_id
    ).offset(offset).limit(limit)

    # Execute the query
    companies_with_acquisitions = session.exec(query).all()
    return companies_with_acquisitions

def get_acquired_companies(session: Session, offset: int, limit: int):
    query = select(Company).join(
        Acquisitions,
        Company.id == Acquisitions.acquired_object_id
    ).offset(offset).limit(limit)

    # Execute query
    companies_got_acquired = session.exec(query).all()
    return companies_got_acquired

def get_company_info(session: Session, company_id: str):
    company = session.query(Company).where(Company.id == company_id).one_or_none()
    if company:
        return company
    raise HTTPException(status_code=404, detail="Company not found")

def get_company_ipo_info(session: Session, company_id: str):
    # Check if the company has gone through an IPO
    company_info = get_company_info(session, company_id)
    ipo_data = company_info.ipos
    return ipo_data

def get_acquired_info(session: Session, company_id: str):
    # check company got acquired by other companies
    company_info = get_company_info(session, company_id)
    acquisition_info = company_info.acquired_companies
    return acquisition_info
    
def get_acquisition_info(session: Session, company_id: str):
    # check company's acquisitions
    company_info = get_company_info(session, company_id)
    acquired_info = company_info.acquiring_companies
    return acquired_info
