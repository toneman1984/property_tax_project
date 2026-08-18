"""
Generate a static table-schema config from full_inventory_scan.json.

This is a one-time (or occasional, if the scan is rerun after TCAD changes
export structure) authoring aid, run by hand -- NOT part of the pipeline
and never regenerated at runtime. Its output, scripts/table_schemas.py, is
a plain checked-in Python file, reviewed like any other code change, that
load_protax_to_sqlite.py imports and trusts.

Usage:
    python -m scripts.schema_codegen
"""

import json
from datetime import datetime

from scripts.utils import PROJECT_ROOT

INVENTORY_FILE = PROJECT_ROOT / "docs" / "tcad_eda" / "full_inventory_scan.json"
OUTPUT_FILE = PROJECT_ROOT / "scripts" / "table_schemas.py"


# ============================================================================
# What to build -- one entry per destination table
# ============================================================================
# "sources": JSON paths (in full_inventory_scan.json's dotted/bracket
#   notation) whose scalar children become this table's columns. Usually
#   one path; property_owners merges two (owners[] itself, plus
#   owners[].ownerValue[] flattened onto the same row, since ownerValue is
#   confirmed always length 1 across the full population).
# "exclude": field names that are genuinely nested sub-structures handled
#   elsewhere (their own table, or deliberately deferred) rather than flat
#   columns -- NOT for excluding scalar fields, those are handled
#   automatically by the nested-vs-scalar heuristic in build_columns_for_source().
# "source_key": the raw JSON key on the parcel record to iterate for a
#   single-level array table (used by scripts.utils.insert_flat_array_rows()).
#   None for tables needing custom traversal (property_owners merges two
#   sources per owner; property_owner_agents needs to iterate agents *within*
#   each owner, not at the record's top level) -- those loaders write their
#   own insert function instead.

TABLE_SPECS = [
    {
        "table": "property_owners",
        "sources": ["owners[]", "owners[].ownerValue[]"],
        "exclude": {"agents", "ownerValue", "ownerTaxable", "exemptions"},
        "source_key": None,
    },
    {"table": "property_owner_agents", "sources": ["owners[].agents[]"], "exclude": set(), "source_key": None},
    {"table": "deeds", "sources": ["deeds[]"], "exclude": set(), "source_key": "deeds"},
    {"table": "sales", "sources": ["sales[]"], "exclude": set(), "source_key": "sales"},
    {"table": "permits", "sources": ["permits[]"], "exclude": set(), "source_key": "permits"},
    {"table": "appeals", "sources": ["appeals[]"], "exclude": set(), "source_key": "appeals"},
    {"table": "taxingunits", "sources": ["taxingunits[]"], "exclude": {"exemptions"}, "source_key": "taxingunits"},
    {"table": "inspections", "sources": ["inspections[]"], "exclude": set(), "source_key": "inspections"},
    {"table": "events", "sources": ["events[]"], "exclude": set(), "source_key": "events"},
    {"table": "tags", "sources": ["tags[]"], "exclude": set(), "source_key": "tags"},
    {"table": "links", "sources": ["links[]"], "exclude": set(), "source_key": "links"},
    {"table": "notes", "sources": ["notes[]"], "exclude": set(), "source_key": "notes"},
    {"table": "smartgroups", "sources": ["smartgroups[]"], "exclude": set(), "source_key": "smartgroups"},
    # Stage 1 "core" child tables -- previously hand-declared in
    # load_protax_to_sqlite.py; converted 2026-08-17 to the same
    # schema-driven pattern as everything above. `properties` itself (the
    # root table) is NOT here -- pID is its literal primary key, not a
    # child array under something, so it stays hand-written.
    {"table": "property_legal_description", "sources": ["propertyLegalDescription[]"], "exclude": set(), "source_key": "propertyLegalDescription"},
    {"table": "property_identification", "sources": ["propertyIdentification[]"], "exclude": set(), "source_key": "propertyIdentification"},
    {"table": "property_characteristics", "sources": ["propertyCharacteristics[]"], "exclude": set(), "source_key": "propertyCharacteristics"},
    {"table": "property_situs", "sources": ["situses[]"], "exclude": set(), "source_key": "situses"},
    {"table": "property_profile", "sources": ["propertyProfile[]"], "exclude": set(), "source_key": "propertyProfile"},
]

# valuations{} is deliberately NOT here -- it's stored whole as a JSON blob
# (property_valuations(pID, valuations_json)), handled directly by the
# loader, not via this column-generation mechanism.
# owners[].ownerTaxable[] is deliberately NOT here -- deferred, see
# docs/tcad_eda/owner_data_structure.md.


# Every nested array object also carries its own redundant `pID` field
# (the parent parcel's ID, duplicated) -- always excluded, since
# create_table_from_schema() already adds a fixed `pID` column. `id` is
# excluded for the same reason against the fixed autoincrement PK. `pYear`
# is excluded for the same reason again, added 2026-08-17 for multi-vintage
# support -- create_table_from_schema() now always adds a fixed `pYear`
# column too (some raw arrays, e.g. appeals/tags, redundantly carry their
# own copy of it).
ALWAYS_EXCLUDE = {"pID", "id", "pYear"}


# ============================================================================
# Type inference
# ============================================================================

def infer_sqlite_type(scalar_type_counts: dict) -> str:
    """
    Widen to the safest common type: any string presence -> TEXT, any float
    -> REAL, int/bool only -> INTEGER, no scalar values ever seen -> TEXT
    (safe default for an always-null-so-far field).
    """
    types = set(scalar_type_counts.keys())
    if not types:
        return "TEXT"
    if "str" in types:
        return "TEXT"
    if "float" in types:
        return "REAL"
    if "int" in types or "bool" in types:
        return "INTEGER"
    return "TEXT"


def build_columns_for_source(fields: dict, source_path: str, exclude: set) -> dict:
    """
    Return {column_name: sqlite_type} for the scalar children of one source
    path, skipping json-string-decode metadata, explicitly excluded nested
    sub-structures, and any field that's predominantly a nested dict/list
    rather than a scalar (majority-nested -> needs its own table or explicit
    handling, not a flat column here).
    """
    columns = {}
    parent = fields.get(source_path)
    if parent is None:
        print(f"  WARNING: source path '{source_path}' not found in inventory scan -- skipping")
        return columns

    for key in parent.get("child_presence_rate", {}):
        if key == "→json" or key in exclude or key in ALWAYS_EXCLUDE:
            continue
        child_path = f"{source_path}.{key}"
        child = fields.get(child_path)
        if child is None:
            continue
        nested = child["dict_visits"] + child["list_visits"]
        if child["total_visits"] and nested > 0.5 * child["total_visits"]:
            continue  # predominantly a nested object/array, not a flat scalar
        columns[key] = infer_sqlite_type(child["scalar_type_counts"])

    return columns


def build_table_schema(fields: dict, spec: dict) -> dict:
    columns = {}
    for source in spec["sources"]:
        columns.update(build_columns_for_source(fields, source, spec["exclude"]))
    return {
        "table": spec["table"],
        "columns": columns,
        "extra_fields": True,
        "source_key": spec["source_key"],
    }


# ============================================================================
# Render
# ============================================================================

def render_schema_file(table_schemas: list, meta: dict) -> str:
    lines = [
        '"""',
        "Static table-schema config, generated by scripts/schema_codegen.py --",
        "DO NOT EDIT BY HAND without regenerating (or document the manual change",
        "here). Consumed by scripts/load_protax_to_sqlite.py via scripts.utils's",
        "create_table_from_schema() / insert_generic_row() / insert_flat_array_rows().",
        "",
        f"Generated {meta['generated_at']} from",
        f"docs/tcad_eda/full_inventory_scan.json (scanned",
        f"{meta['records_scanned']:,} records on {meta['scan_date']}).",
        '"""',
        "",
        "TABLE_SCHEMAS = [",
    ]
    for schema in table_schemas:
        lines.append("    {")
        lines.append(f'        "table": {schema["table"]!r},')
        lines.append('        "columns": {')
        for col, sql_type in schema["columns"].items():
            lines.append(f"            {col!r}: {sql_type!r},")
        lines.append("        },")
        lines.append(f'        "extra_fields": {schema["extra_fields"]!r},')
        lines.append(f'        "source_key": {schema["source_key"]!r},')
        lines.append("    },")
    lines.append("]")
    lines.append("")
    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================

def run():
    if not INVENTORY_FILE.exists():
        raise FileNotFoundError(
            f"Inventory scan not found: {INVENTORY_FILE}\n"
            f"  Run 'python -m scripts.inventory_scan_full' first."
        )

    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]
    scan_meta = data["_meta"]

    table_schemas = []
    for spec in TABLE_SPECS:
        schema = build_table_schema(fields, spec)
        table_schemas.append(schema)
        print(f"  {schema['table']}: {len(schema['columns'])} columns")

    meta = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "records_scanned": scan_meta["records_scanned"],
        "scan_date": scan_meta["scan_date"],
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(render_schema_file(table_schemas, meta))

    print(f"\nWrote {OUTPUT_FILE} ({len(table_schemas)} tables)")


if __name__ == "__main__":
    run()
