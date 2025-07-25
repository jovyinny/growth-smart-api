"""Databse.

The database should, handle the following
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel

from .config import engine


def generate_ids() -> str:
    return str(uuid4())


class User(SQLModel, table=True):
    """User table."""

    id: str = Field(
        min_length=20,
        default_factory=lambda: generate_ids(),
        unique=True,
        primary_key=True,
    )
    name: str
    phone_number: str = Field(
        min_length=10,
        max_length=12,
        unique=True,
        index=True,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()"},
    )


class Buyer(SQLModel, table=True):
    """Buyer table."""

    id: str = Field(
        min_length=20,
        default_factory=lambda: generate_ids(),
        unique=True,
        primary_key=True,
    )
    user_id: str = Field(foreign_key="user.id")


class Farmer(SQLModel, table=True):
    """Farmer table."""

    id: str = Field(
        min_length=20,
        default_factory=lambda: generate_ids(),
        unique=True,
        primary_key=True,
    )
    user_id: str = Field(foreign_key="user.id")
    region: str
    latitude: float
    longitude: float
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"server_default": "now()"},
    )


class Crop(SQLModel, table=True):
    """Farmer crops."""

    id: str = Field(
        min_length=20,
        default_factory=lambda: generate_ids(),
        unique=True,
        primary_key=True,
    )
    farmer_id: str = Field(foreign_key="farmer.id")
    active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    name: str
    category: str
    tag: Optional[str] = Field(
        default=None,
    )
    price: float
    value: float = Field(description="Value of the crop size eg 10 for the given price")
    unit: str = Field(description="Unit value eg KG, Visado")
    description: Optional[str] = Field(
        default=None,
    )


class Order(SQLModel, table=True):
    """Order table."""

    id: str = Field(
        default_factory=generate_ids(),
        unique=True,
        primary_key=True,
    )
    buyer_id: str = Field(foreign_key="buyer.id")
    farmer_id: str = Field(foreign_key="farmer.id")
    total_amount: float
    order_status: str
    payment_status: str
    fulfillment_status: str


SQLModel.metadata.create_all(engine)
