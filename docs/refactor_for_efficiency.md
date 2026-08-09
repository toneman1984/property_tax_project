# Refactor for Efficiency: Shared Helper Module

**Status:** Planned — not yet implemented. This is a sketch to work from, not
a commitment to the exact contents below.

## Motivation

`load_protax_to_sqlite.py` and `load_owners_to_sqlite.py` currently each
define their own copies of `format_time()` and `format_size()` — identical
code, duplicated because `load_owners_to_sqlite.py` was written by copying
the pattern rather than importing it. As more stage scripts get added
(Stage 4's remaining pieces, and whatever comes after), this duplication
will keep growing unless there's a shared place for genuinely
general-purpose helpers to live.

Script-specific helpers (e.g. `pick_primary_owner()`, `insert_owner()`) stay
where they are — they're coupled to what each script is doing and don't
belong in a shared module.

## Sketch

### 1. New file: `scripts/utils.py`

```python
"""
Shared helpers used across multiple pipeline scripts.

Anything here should be general-purpose (formatting, small conversions) —
script-specific logic stays in its own script.
"""

from decimal import Decimal


def format_time(seconds):
    """Format seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def format_size(bytes_size):
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
    return value


def get_value(record, key, default=None):
    """Safely get a value from a record, converting types as needed."""
    value = record.get(key, default)
    return convert_value(value)
```

`format_time`/`format_size` are the clear, uncontroversial move — pure
formatting, identical in both scripts today. `convert_value`/`get_value`
are included too since they're *also* duplicated verbatim between the two
loader scripts, but they're arguably more "domain" than "generic" (SQLite +
Decimal specific) — worth a deliberate yes/no rather than assuming.

### 2. Updated imports in the scripts that use them

```python
# load_protax_to_sqlite.py / load_owners_to_sqlite.py
from scripts.utils import format_time, format_size, convert_value, get_value
```

Each script drops its own copies of these four functions once the import is
in place.

### 3. Invocation convention change

This is the part that actually requires a decision, not just code motion.

`from scripts.utils import ...` is a *package-relative* import — it only
resolves if the `scripts` package's parent directory (the project root) is
on Python's import path. That's already true in the two contexts these
scripts mainly run in today:

- `python main.py` — imports scripts as `from scripts.X import run`, run
  from the project root
- Positron's interactive console — working directory is the project root

It is **not** true if a script is run directly as a bare file:

```
python scripts/load_owners_to_sqlite.py     # breaks — scripts/ has no
                                              # parent on the import path
```

Every script's docstring currently documents that bare-file form as the
`Usage:` example. To keep standalone single-stage runs working (useful
during development, without rerunning the whole pipeline), the convention
needs to switch to running scripts as modules instead:

```
python -m scripts.load_owners_to_sqlite
```

`-m` tells Python to resolve `scripts.load_owners_to_sqlite` as a package
import first, which puts the project root on the path automatically — same
mechanism that already makes `main.py`'s imports work.

## Progress Tracker

- [ ] 1. Create `scripts/utils.py` (decide scope: formatting-only, or also
      `convert_value`/`get_value`)
- [ ] 2. Update `load_protax_to_sqlite.py` to import from `scripts.utils`,
      remove its local copies
- [ ] 3. Update `load_owners_to_sqlite.py` to import from `scripts.utils`,
      remove its local copies
- [ ] 4. Update each script's `Usage:` docstring to the `python -m
      scripts.X` form
- [ ] 5. Update `README.md` if it documents single-stage invocation anywhere

## Open Questions

- Should `PROJECT_ROOT` resolution also move into `scripts/utils.py`? Since
  `Path(__file__)` inside `utils.py` would resolve to the same project root
  regardless of which script imports it, this is technically consolidatable
  too — deferred here since it's a separate decision from the formatting
  helpers that prompted this doc.
- Apply now, or bundle into the Stage 4 pipeline-wiring step (Step 5 in
  `docs/fraud_model_plan.md`), since that step already touches every
  script's entry-point pattern?
