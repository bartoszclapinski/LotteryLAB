from __future__ import annotations
from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select, and_, desc, func
from sqlalchemy.orm import Session

from src.database.models import Draw


class DrawRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        game_type: Optional[str] = None,
        game_provider: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        stmt = select(Draw)
        conditions = []
        if game_type:
            conditions.append(Draw.game_type == game_type)
        if game_provider:
            conditions.append(Draw.game_provider == game_provider)
        if date_from:
            conditions.append(Draw.draw_date >= date_from)
        if date_to:
            conditions.append(Draw.draw_date <= date_to)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(Draw.draw_date.desc(), Draw.draw_number.desc())
        rows = self.session.execute(stmt).scalars().all()

        # Convert to dictionaries with proper date formatting
        result = []
        for row in rows[offset: offset + limit]:
            result.append({
                "id": row.id,
                "draw_number": row.draw_number,
                "draw_date": row.draw_date.isoformat(),
                "game_type": row.game_type,
                "game_provider": row.game_provider,
                "numbers": row.numbers,
                "jackpot": row.jackpot,
            })
        return result

    def count(
        self,
        game_type: Optional[str] = None,
        game_provider: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> int:
        conditions = []
        if game_type:
            conditions.append(Draw.game_type == game_type)
        if game_provider:
            conditions.append(Draw.game_provider == game_provider)
        if date_from:
            conditions.append(Draw.draw_date >= date_from)
        if date_to:
            conditions.append(Draw.draw_date <= date_to)
        stmt = select(func.count()).select_from(Draw)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        return int(self.session.execute(stmt).scalar_one() or 0)

    def latest(self, limit: int = 20) -> list[dict]:
        stmt = select(Draw).order_by(desc(Draw.draw_number)).limit(limit)
        rows = self.session.execute(stmt).scalars().all()

        # Convert to dictionaries
        result = []
        for row in rows:
            result.append({
                "id": row.id,
                "draw_number": row.draw_number,
                "draw_date": row.draw_date.isoformat(),
                "game_type": row.game_type,
                "game_provider": row.game_provider,
                "numbers": row.numbers,
                "jackpot": row.jackpot,
            })
        return result
