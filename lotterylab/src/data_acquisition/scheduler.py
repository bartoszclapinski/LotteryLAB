from __future__ import annotations
from typing import Iterable, Tuple, Dict
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime, UTC
from pathlib import Path
import hashlib
import csv

from sqlalchemy import select, func

from src.database.session import SessionLocal
from src.database.models import Draw
from src.data_acquisition.file_parser import parse_initial_txt
from src.data_acquisition.data_validator import validate_draw, serialize_numbers
from src.utils.normalizer import normalize_game_type
from src.utils.logger import get_logger

RAW_DIR = Path(__file__).resolve().parents[2] / ".data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
UPDATE_LOG_PATH = Path(__file__).resolve().parents[2] / ".data" / "update_log.csv"
UPDATE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_DIR = Path(__file__).resolve().parents[2] / ".logs"
LOGGER = get_logger("scheduler", log_file=str(LOG_DIR / "scheduler.log"))


def _latest_raw_file() -> Path | None:
    files = sorted(RAW_DIR.glob("mbnet_*.txt"), key=lambda p: p.name, reverse=True)
    return files[0] if files else None


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _enforce_retention(max_keep: int = 30) -> None:
    files = sorted(RAW_DIR.glob("mbnet_*.txt"), key=lambda p: p.name, reverse=True)
    for p in files[max_keep:]:
        try:
            p.unlink(missing_ok=True)
            LOGGER.info("raw_retention_deleted file=%s", p.name)
        except Exception as e:
            LOGGER.warning("raw_retention_delete_failed file=%s error=%s", p.name, e)


def fetch_mbnet_txt(url: str, timeout: int = 20, archive: bool = True) -> Tuple[list[str], Dict[str, str]]:
    LOGGER.info("fetch_start url=%s", url)
    try:
        with urlopen(url, timeout=timeout) as resp:
            data = resp.read()
    except (URLError, HTTPError) as e:
        LOGGER.error("fetch_failed url=%s error=%s", url, e)
        raise RuntimeError(f"Failed to fetch MBNet data: {e}")

    sha256 = _sha256_bytes(data)
    saved_name = ""

    if archive:
        same_as_latest = False
        latest = _latest_raw_file()
        if latest and latest.exists():
            try:
                latest_bytes = latest.read_bytes()
                same_as_latest = (_sha256_bytes(latest_bytes) == sha256)
            except Exception as ex:
                LOGGER.warning("raw_compare_failed file=%s error=%s", latest.name, ex)
                same_as_latest = False
        if not same_as_latest:
            ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
            saved = RAW_DIR / f"mbnet_{ts}.txt"
            saved.write_bytes(data)
            saved_name = saved.name
            LOGGER.info("raw_saved file=%s sha256=%s", saved_name, sha256)
            _enforce_retention(30)
        else:
            LOGGER.info("raw_duplicate_detected sha256=%s", sha256)

    # try utf-8 then latin-1
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    LOGGER.info("fetch_ok url=%s lines=%d sha256=%s file=%s", url, len(lines), sha256, saved_name)
    return lines, {"file": saved_name, "sha256": sha256}


def import_new_from_lines(lines: Iterable[str], game_provider: str = "pl_totalizator") -> dict:
    LOGGER.info("import_start provider=%s", game_provider)
    inserted = 0
    skipped = 0
    with SessionLocal() as session:
        max_id = session.execute(select(func.max(Draw.draw_number))).scalar() or 0
        LOGGER.info("import_state max_existing=%d", max_id)
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
                LOGGER.info("import_progress inserted=%d skipped=%d", inserted, skipped)
        session.commit()
    LOGGER.info("import_done inserted=%d skipped=%d", inserted, skipped)
    return {"inserted": inserted, "skipped": skipped, "max_existing": max_id}


def _append_update_log(source_url: str, meta: Dict[str, str], res: dict) -> None:
    new_file = not UPDATE_LOG_PATH.exists()
    with UPDATE_LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["timestamp_utc", "source_url", "inserted", "skipped", "max_existing", "file_name", "sha256"])
        w.writerow([
            datetime.now(UTC).isoformat(),
            source_url,
            res.get("inserted", 0),
            res.get("skipped", 0),
            res.get("max_existing", 0),
            meta.get("file", ""),
            meta.get("sha256", ""),
        ])
    LOGGER.info("update_log_appended url=%s inserted=%s skipped=%s file=%s", source_url, res.get("inserted"), res.get("skipped"), meta.get("file"))


def update_from_mbnet(url: str = "http://www.mbnet.com.pl/dl_razem.txt", game_provider: str = "pl_totalizator") -> dict:
    LOGGER.info("update_start url=%s provider=%s", url, game_provider)
    lines, meta = fetch_mbnet_txt(url)
    res = import_new_from_lines(lines, game_provider=game_provider)
    _append_update_log(url, meta, res)
    LOGGER.info("update_done url=%s inserted=%s skipped=%s", url, res.get("inserted"), res.get("skipped"))
    return res
