#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from start_bfsi_frontend import start_bfsi_frontend  # noqa: E402

if __name__ == "__main__":
    start_bfsi_frontend()
