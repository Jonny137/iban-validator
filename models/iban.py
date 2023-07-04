import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Enum

from db.base_class import Base, UtcNow


class Iban(Base):
    __tablename__ = 'iban'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4
    )
    iban = Column(String(), index=True)
    status = Column(Enum('valid', 'invalid', name='iban_status'))
    created_at = Column(DateTime(timezone=True), server_default=UtcNow())
    modified_at = Column(DateTime(timezone=True), onupdate=UtcNow())
