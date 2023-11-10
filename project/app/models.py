from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Define the data models

class CompanyBase(SQLModel):
    name: str = Field(index=True)

class IposBase(SQLModel):
    valuation_amount: str
    valuation_currency_code: str
    raised_amount: str
    raised_currency_code: str
    public_at: str
    stock_symbol: str
    source_url: str
    source_description: str

class AcquisitionsBase(SQLModel):
    price_amount: str = Field(nullable=True)
    price_currency_code: str
    acquired_at: str
    source_url: str
    source_description: str = Field(nullable=False)

# Define table models
class Company(CompanyBase, table=True):
    id: str = Field(primary_key=True)
    homepage_url: str
    overview: str
    country_code: str = Field(index=True)
    entity_type: str
    entity_id: str
    state_code: str
    city: str


    ipos: List["Ipos"] = Relationship(back_populates="company")
    acquiring_companies: List["Acquisitions"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Acquisitions.acquiring_object_id==Company.id"})
    acquired_companies: List["Acquisitions"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Acquisitions.acquired_object_id==Company.id"})

class Ipos(IposBase, table=True):
    id: int = Field(primary_key=True)
    ipo_id: int
    object_id: str = Field(default=None, foreign_key="company.id")
    
    company: Optional[Company] = Relationship(back_populates="ipos")

class Acquisitions(AcquisitionsBase, table=True):
    id: int = Field(primary_key=True)
    acquisition_id: int

    acquiring_object_id: Optional[str] = Field(default=None, foreign_key="company.id", nullable=True)
    acquired_object_id: Optional[str] = Field(default=None, foreign_key="company.id", nullable=True)

    acquiring_company: Optional[Company] = Relationship(sa_relationship_kwargs={"primaryjoin": "Acquisitions.acquiring_object_id==Company.id", "lazy": "joined", "overlaps": "acquiring_companies"})
    acquired_company: Optional[Company] = Relationship(sa_relationship_kwargs={"primaryjoin": "Acquisitions.acquired_object_id==Company.id", "lazy": "joined", "overlaps": "acquired_companies"})


# Define Response Models
class CompanyResponse(CompanyBase):
    id: str
    homepage_url: str
    overview: str
    country_code: str

class IposResponse(IposBase):
    id: int

class AcquisitionResponse(AcquisitionsBase):
    id: int
    acquired_company: Optional[CompanyBase]

class AcquiredResponse(AcquisitionsBase):
    id: int
    acquiring_company: Optional[CompanyBase]
