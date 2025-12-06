from __future__ import annotations
from collections import Counter
from sqlalchemy import select
from src.database.session import SessionLocal
from src.database.models import Draw

def main() -> None:
    with SessionLocal() as s:
        rows = s.execute(select(Draw.draw_date, Draw.game_type)).all()
    counter = Counter(rows)
    dups = [(k, c) for k, c in counter.items() if c > 1]
    dups.sort(key=lambda x: (x[0][0], x[0][1]))
    print({"duplicate_pairs": len(dups)})
    for (draw_date, game_type), count in dups[:25]:
        print(f"{draw_date} {game_type}: {count}")

if __name__ == "__main__":
    main()
