"""
Models for the service table.
"""

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import String


class State(SQLModel, table=True):
    """
    A state is a state in the United States.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String)
    abbreviation: str = Field(sa_type=String, index=True)
    fips_code: int = Field(index=True)
    providers: list["Provider"] = Relationship(back_populates="state")


class Provider(SQLModel, table=True):
    """
    A provider is a healthcare provider that is part of the Medicare program.
    """

    id: int | None = Field(default=None, primary_key=True)
    ccn: int = Field(index=True)
    name: str = Field(sa_type=String, index=True)
    city: str = Field(sa_type=String, index=True)
    state_id: int | None = Field(default=None, foreign_key="state.id")
    state: State = Relationship(back_populates="providers")
    zip_code_five: str = Field(sa_type=String, index=True)
    rural_commuting_area: int | None = Field(default=None, index=True)
    rural_commuting_area_description: str = Field(index=True)

    services: list["Service"] = Relationship(back_populates="provider")


class Service(SQLModel, table=True):
    """
    A service is a healthcare service that is part of the Medicare program.
    """

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(sa_type=String, index=True)
    discharges: int = Field(index=True)
    average_covered_charges: float = Field(index=True)
    average_total_payments: float = Field(index=True)
    average_medicare_payments: float = Field(index=True)
    provider_id: int | None = Field(default=None, foreign_key="provider.id")

    provider: Provider = Relationship(back_populates="services")
