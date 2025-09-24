from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, JSON, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_name: Mapped[str] = mapped_column(Text, nullable=False)
    legal_name: Mapped[str] = mapped_column(Text, nullable=False)
    cnpj: Mapped[str | None] = mapped_column(String(18), unique=True)
    website: Mapped[str | None] = mapped_column(Text)
    phone: Mapped[str | None] = mapped_column(Text)
    address: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
