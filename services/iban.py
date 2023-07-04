import string
import logging
from itertools import chain

from sqlalchemy import desc
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.iban import Iban
from schemas.iban import IbanCreate

logger = logging.getLogger(__name__)

_LETTERS = chain(enumerate(string.digits + string.ascii_uppercase),
                 enumerate(string.ascii_lowercase, 10))
LETTERS = {ord(d): str(i) for i, d in _LETTERS}
ME_COUNTRY_CODE = 'ME'
ME_IBAN_LEN = 22


def _number_iban(iban):
    return (iban[4:] + iban[:4]).translate(LETTERS)


def _generate_iban_check_digits(iban):
    number_iban = _number_iban(iban[:2] + '00' + iban[4:])
    return '{:0>2}'.format(98 - (int(number_iban) % 97))


def _valid_iban(iban):
    return int(_number_iban(iban)) % 97 == 1


def validate_iban(db: Session, iban: IbanCreate):
    # remove redundant whitespaces firstly
    joint_iban = ''.join(iban.iban.split())
    try:
        # Perform check for ME country code
        if iban.iban[0:2].upper() != ME_COUNTRY_CODE:
            logger.warning(
                'IBAN does not posses Montenegro country abbreviation!'
            )
            raise HTTPException(
                status_code=400,
                detail='Invalid IBAN for Montenegro.'
            )

        # Perform check for size of ME IBAN
        if len(joint_iban) != ME_IBAN_LEN:
            logger.warning(
                'IBAN size for Montenegro is invalid!'
            )
            raise HTTPException(
                status_code=400,
                detail='Invalid IBAN for Montenegro.'
            )

        # Since we now know that IBAN is from ME and of right size, perform
        # standard algorithm to check whether it's valid
        new_iban = Iban(iban=joint_iban, status='invalid')
        if (
                _generate_iban_check_digits(joint_iban) == joint_iban[2:4] and
                _valid_iban(joint_iban)
        ):
            logger.info('Successfully validated IBAN: {}'.format(joint_iban))
            new_iban.status = 'valid'
        db.add(new_iban)
        db.commit()
        db.refresh(new_iban)
    except ValueError as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail='Invalid literal for parsing.'
        )

    return new_iban


def get_last_ten_ibans(db: Session):
    iban_list = db.query(Iban).order_by(desc(Iban.created_at)).limit(10).all()

    return iban_list
