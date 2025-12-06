from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lotterylab.db")
ENV = os.getenv("ENV", "dev")
