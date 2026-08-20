from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint("canonical_url", name="uq_company_canonical_url"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    website: Mapped[str] = mapped_column(String(500))
    canonical_url: Mapped[str] = mapped_column(String(500), index=True)
    description: Mapped[str | None] = mapped_column(Text())
    careers_url: Mapped[str | None] = mapped_column(String(500))
    discovered_from: Mapped[str] = mapped_column(String(500))
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    people: Mapped[list["Person"]] = relationship(back_populates="company", cascade="all, delete-orphan")


class Person(Base):
    __tablename__ = "people"
    __table_args__ = (UniqueConstraint("company_id", "name", "role", name="uq_company_person_role"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    role: Mapped[str] = mapped_column(String(255), index=True)
    source_url: Mapped[str] = mapped_column(String(500))
    confidence: Mapped[int] = mapped_column(default=50)
    verified_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company: Mapped[Company] = relationship(back_populates="people")
