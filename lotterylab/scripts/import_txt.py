from __future__ import annotations
import argparse
from pathlib import Path
import sys
from collections import defaultdict
from sqlalchemy import select

# Ensure the parent directory that contains the 'src' package is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database.session import SessionLocal
from src.database.models import Draw
from src.data_acquisition.file_parser import parse_initial_txt
from src.data_acquisition.data_validator import validate_draw, serialize_numbers
from src.utils.normalizer import normalize_game_type
from src.utils.logger import get_logger

LOGGER = get_logger("import_txt", log_file=str(PROJECT_ROOT / ".logs" / "import_txt.log"))


def upsert_draw(session, draw: Draw) -> None:
    existing = session.execute(select(Draw).where(Draw.draw_number == draw.draw_number)).scalar_one_or_none()
    if existing is None:
        session.add(draw)
    else:
        existing.draw_date = draw.draw_date
        existing.game_type = draw.game_type
        existing.game_provider = draw.game_provider
        existing.numbers = draw.numbers
        existing.jackpot = draw.jackpot


def main() -> None:
    parser = argparse.ArgumentParser(description="Import Lotto TXT data into DB")
    parser.add_argument("path", help="Path to TXT file")
    parser.add_argument("--game", dest="game_type", default=None, help="Game type label override")
    parser.add_argument("--provider", dest="game_provider", default="pl_totalizator", help="Game provider id")
    args = parser.parse_args()

    total = 0
    ok = 0
    skipped = 0
    per_date_count: dict[str, int] = defaultdict(int)

    LOGGER.info("import_cli_start path=%s provider=%s game=%s", args.path, args.game_provider, args.game_type)
    with open(args.path, "r", encoding="utf-8") as f, SessionLocal() as session:
        for parsed in parse_initial_txt(f):
            total += 1
            result = validate_draw(parsed)
            if not result.ok:
                skipped += 1
                continue

            # Determine game_type
            game_type = args.game_type
            if game_type is None:
                key = parsed.draw_date.isoformat()
                idx = per_date_count[key]
                game_type = "lotto" if idx == 0 else "lotto_plus"
                per_date_count[key] += 1
            game_type = normalize_game_type(game_type, args.game_provider)

            model = Draw(
                draw_number=parsed.draw_number,
                draw_date=parsed.draw_date,
                game_type=game_type,
                game_provider=args.game_provider,
                numbers=serialize_numbers(parsed.numbers),
                jackpot=None,
            )
            upsert_draw(session, model)
            if total % 500 == 0:
                session.commit()
                LOGGER.info("import_cli_progress total=%d inserted_or_updated=%d skipped=%d", total, ok, skipped)
            ok += 1
        session.commit()
    LOGGER.info("import_cli_done total=%d inserted_or_updated=%d skipped=%d", total, ok, skipped)
    print({"total": total, "inserted_or_updated": ok, "skipped": skipped})


if __name__ == "__main__":
    main()
