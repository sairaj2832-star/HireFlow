"""Synthetic-only purge — TTL 12mo, runs nightly (B0 stub, B7 wires job)."""

from pathlib import Path
from typing import Union

RETENTION_DAYS = 365  # MASTER §37 / Report §10 DQ14


def purge_expired(db_path: Union[Path, None] = None) -> int:
    """B7: delete source_records where retention_until < now(). B0: no-op with correct TTL constant."""
    return 0
