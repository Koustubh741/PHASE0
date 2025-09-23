#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from simple_backend_server import app  # noqa: E402

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
