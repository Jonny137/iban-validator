from typing import Any, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from dependencies import get_db
from schemas.iban import IbanCreate, Iban
from services.iban import validate_iban, get_last_ten_ibans

iban_router = APIRouter()


@iban_router.post('/', response_model=Iban)
def validate_iban_and_register_it(
    iban: IbanCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Validate given IBAN and add the it to the database.

    :param iban: IBAN (International Bank Account Number)
    :param db: Current database session
    :returns: Newly created expense
    """
    response = validate_iban(db=db, iban=iban)
    return response


@iban_router.get('/tail', response_model=List[Iban])
def get_ibans(db: Session = Depends(get_db)) -> Any:
    """
    Fetch last 10 IBANs from the database.

    :param db: Current database session
    :returns: List of IBANs
    """
    response = get_last_ten_ibans(db=db)
    return response
