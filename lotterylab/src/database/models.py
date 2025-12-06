from __future__ import annotations
from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Integer, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base

class Draw(Base):
    __tablename__ = "draws"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    draw_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    draw_date: Mapped[date] = mapped_column(Date, nullable=False)
    game_type: Mapped[str] = mapped_column(String(20), nullable=False)
    game_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    numbers: Mapped[str] = mapped_column(String, nullable=False)
    jackpot: Mapped[Optional[float]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class NumberStatistics(Base):
    __tablename__ = "number_statistics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    game_type: Mapped[str] = mapped_column(String(20), nullable=False)
    total_appearances: Mapped[int] = mapped_column(Integer, default=0)
    last_appearance: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    average_gap_days: Mapped[Optional[float]] = mapped_column(nullable=True)
    max_gap_days: Mapped[Optional[int]] = mapped_column(nullable=True)
    min_gap_days: Mapped[Optional[int]] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    analysis_type: Mapped[str] = mapped_column(String(50), nullable=False)
    parameters: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    results: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
