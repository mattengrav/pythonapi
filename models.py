
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from pydantic import BaseModel
import datetime

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mortgage_db" #Type of db/username/password @ db address

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


class Mortgage(Base):
    __tablename__ = "mortgages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True, autoincrement=True)

    principal: Mapped[float] = mapped_column(nullable=False)
    apr: Mapped[float] = mapped_column(nullable=False)
    term: Mapped[int] = mapped_column(nullable=False)

    

class ExtraPayments(Base):
    __tablename__ = "extraPayments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    foreignID: Mapped[int] = mapped_column(ForeignKey("mortgages.id"), unique=False)
#Reaccuring additional payment
    extra_payment: Mapped[float]
    extra_payment_start_month: Mapped[datetime.date]

#Lump sum payments
    extra_payments_month: Mapped[datetime.date]
    extra_payments_amount: Mapped[float]


    # Request Model for Loan Calculation
class LoanRequest(BaseModel):
    principal: float
    term: int  # Years
    apr: float

# Response Model
class LoanResponse(BaseModel):
    id: int

Base.metadata.create_all(bind=engine)