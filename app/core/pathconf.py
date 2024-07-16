import os
from pathlib import Path

BasePath = Path(__file__).resolve().parent.parent
ALEMBIC_Versions_DIR = os.path.join(BasePath, 'alembic', 'versions')
LOG_DIR = os.path.join(BasePath, 'log')
SQLITE_DATABASE_FILE = f"sqlite:///{os.path.join(BasePath, 'local.db')}"
