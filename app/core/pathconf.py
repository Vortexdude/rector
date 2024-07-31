import os
from pathlib import Path

__all__ = ["BasePath", "SQLITE_DATABASE_FILE"]

BasePath = Path(__file__).resolve().parent.parent
ALEMBIC_VERSION_DIR = os.path.join(BasePath, 'alembic', 'versions')
LOG_DIR = os.path.join(BasePath, 'log')
SQLITE_DATABASE_FILE = f"sqlite:///{os.path.join(BasePath, 'local.db')}"
