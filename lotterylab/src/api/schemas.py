from __future__ import annotations
from pydantic import BaseModel
from datetime import date
from typing import Optional

class DrawOut(BaseModel):
    id: int
    draw_number: int
    draw_date: str  # Keep as string for JSON compatibility
    game_type: str
    game_provider: Optional[str]
    numbers: str
    jackpot: Optional[float]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        """Convert ORM object to Pydantic model with proper date formatting."""
        data = super().from_orm(obj)
        if hasattr(data, 'draw_date') and isinstance(data.draw_date, date):
            data.draw_date = data.draw_date.isoformat()
        return data

class DrawListOut(BaseModel):
    items: list[DrawOut]
    total: int
