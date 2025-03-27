from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.params import Body
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import json

from models import *

import logging #logger to debug
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


DATABASE_URL = "postgresql://postgres:postgres@localhost/mortgage_db" #Type of db/username/password @ db address

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database tables if they don't already exist, normally use migrations


app = FastAPI()
origins = [
    "http://localhost:63342/calculate",
    "http://localhost:63342/mortgage_website/",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/calculate")
def calculate_loan(data: LoanRequest, db: Session = Depends(get_db)):
    logger.debug("Calculate loan function running")
    principal = data.principal
    term = data.term * 12  # Convert years to months
    apr = data.apr / 100 / 12  # Convert annual rate to monthly decimal

    # Monthly payment formula
    if apr > 0:
        monthly_payment = round(principal * (apr * (1 + apr) ** term) / ((1 + apr) ** term - 1), 2)
    else:
        monthly_payment = round(principal / term, 2)



    # Save to Database
    loan_entry = Mortgage(
        principal = principal,
        term = term,
        apr = data.apr
    )

    db.add(loan_entry)
    db.commit()
    db.refresh(loan_entry)

    return {}
