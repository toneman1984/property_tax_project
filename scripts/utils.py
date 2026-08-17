"""
Shared helpers used across multiple pipeline scripts.

Anything here should be general-purpose (formatting, small conversions,
generic file validation) — schema, SQL, and business logic specific to one
script stays in that script.
"""

import json
import re
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def format_time(seconds: float) -> str:
    """Format seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def format_size(bytes_size: float) -> str:
    """Format bytes into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f}TB"


def convert_value(value):
    """Convert Decimal and other unsupported types for SQLite."""
    if value is None:
        return None
    if isinstance(value, Decimal):
        return int(value) if value == int(value) else float(value)
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    return value


def get_value(record: dict, key: str, default=None):
    """Safely get a value from a record, converting types as needed."""
    value = record.get(key, default)
    return convert_value(value)


def optimize_for_bulk_insert(conn) -> None:
    """Configure SQLite for fast bulk inserts."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA cache_size = -64000")  # 64MB cache
    cursor.execute("PRAGMA temp_store = MEMORY")
    conn.commit()


def validate_json_file(json_file: Path, min_size_gb: float = 10.0) -> None:
    """
    Check a TCAD JSON source file before loading. Raises on hard failures
    (missing file, implausibly small file); warns on soft ones (stale export)
    without blocking.
    """
    if not json_file.exists():
        raise FileNotFoundError(
            f"Source JSON not found: {json_file}\n"
            f"  Run 'python scripts/fetch_tcad.py' to download it."
        )

    size_gb = json_file.stat().st_size / (1024 ** 3)
    if size_gb < min_size_gb:
        raise ValueError(
            f"JSON file is only {size_gb:.1f} GB — expected ~29 GB.\n"
            f"  This likely indicates an incomplete download.\n"
            f"  Delete the file and run 'python scripts/fetch_tcad.py' to re-download."
        )
    print(f"  JSON file: {json_file.name} ({size_gb:.1f} GB)")

    match = re.search(r'(\d{8})', json_file.name)
    if match:
        try:
            file_date = datetime.strptime(match.group(1), '%Y%m%d').date()
            age_days = (date.today() - file_date).days
            if age_days > 180:
                print(f"  WARNING: Export is {age_days} days old (dated {file_date}).")
                print("  A newer TCAD export may be available at traviscad.org.")
                print("  Update SELECTED_EXPORT in fetch_tcad.py and re-run it to refresh.")
        except ValueError:
            pass
