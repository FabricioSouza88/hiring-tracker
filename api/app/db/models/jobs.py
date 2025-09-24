from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.models.companies import Base

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    test_description: Mapped[str | None] = mapped_column(Text)
    seniority: Mapped[str | None] = mapped_column(String(32))
    location_type: Mapped[str | None] = mapped_column(String(32))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
