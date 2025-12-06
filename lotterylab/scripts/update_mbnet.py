from __future__ import annotations
from pathlib import Path
import sys
import argparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_acquisition.scheduler import update_from_mbnet  # type: ignore


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and import new draws from MBNet")
    parser.add_argument("--url", default="http://www.mbnet.com.pl/dl_razem.txt")
    parser.add_argument("--provider", default="pl_totalizator")
    args = parser.parse_args()
    res = update_from_mbnet(url=args.url, game_provider=args.provider)
    print(res)


if __name__ == "__main__":
    main()
