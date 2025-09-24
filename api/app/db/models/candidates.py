from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, JSON, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.models.companies import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    cpf: Mapped[str | None] = mapped_column(String(14), unique=True)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(Text)
    address: Mapped[dict | None] = mapped_column(JSON)
    profile_summary: Mapped[str | None] = mapped_column(Text)
    presentation_text: Mapped[str | None] = mapped_column(Text)
    linkedin_url: Mapped[str | None] = mapped_column(Text)
    github_url: Mapped[str | None] = mapped_column(Text)
    resume_file_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id"))
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
