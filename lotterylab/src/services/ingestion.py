from __future__ import annotations
from typing import Iterable, Dict
from pathlib import Path
from datetime import date

from sqlalchemy import select, func

from src.database.session import SessionLocal
from src.database.models import Draw
from src.data_acquisition.file_parser import parse_initial_txt
from src.data_acquisition.data_validator import validate_draw, serialize_numbers
from src.utils.normalizer import normalize_game_type
from src.data_acquisition.scheduler import update_from_mbnet


def import_lines(lines: Iterable[str], game_provider: str = "pl_totalizator") -> Dict[str, int]:
    inserted = 0
    skipped = 0
    with SessionLocal() as session:
        max_id = session.execute(select(func.max(Draw.draw_number))).scalar() or 0
        per_date_count: dict[str, int] = {}
        for parsed in parse_initial_txt(lines):
            if parsed.draw_number <= max_id:
                skipped += 1
                continue
            vr = validate_draw(parsed)
            if not vr.ok:
                skipped += 1
                continue
            key = parsed.draw_date.isoformat()
            idx = per_date_count.get(key, 0)
            game_type = "lotto" if idx == 0 else "lotto_plus"
            per_date_count[key] = idx + 1
            game_type = normalize_game_type(game_type, game_provider)
            session.add(
                Draw(
                    draw_number=parsed.draw_number,
                    draw_date=parsed.draw_date,
                    game_type=game_type,
                    game_provider=game_provider,
                    numbers=serialize_numbers(parsed.numbers),
                    jackpot=None,
                )
            )
            inserted += 1
            if inserted % 500 == 0:
                session.commit()
        session.commit()
    return {"inserted": inserted, "skipped": skipped}


def import_file(path: str | Path, game_provider: str = "pl_totalizator") -> Dict[str, int]:
    p = Path(path)
    content = p.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return import_lines(lines, game_provider=game_provider)


def incremental_update_from_mbnet(url: str = "http://www.mbnet.com.pl/dl_razem.txt", game_provider: str = "pl_totalizator") -> dict:
    return update_from_mbnet(url=url, game_provider=game_provider)
