"""
One-time investigative script: recursively scans the full TCAD JSON export
and builds a complete field inventory (presence rate, population rate,
inferred type(s), array-length distribution, examples) across the full
486,859-parcel population, at every nesting depth -- including
string-encoded JSON sub-documents (e.g. `events[].eventData`,
`appeals[].claimantEvidence`), which are detected and recursed into like
any other nested structure.

NOT part of the pipeline (main.py doesn't import this). Run directly:

    python -m scripts.inventory_scan_full --limit 30000   # timing test
    python -m scripts.inventory_scan_full                 # full run
    python -m scripts.inventory_scan_full --resume         # resume a full run

NOTE on performance: the conda-forge build of ijson has no compiled backend
and silently falls back to its pure-Python parser, which is roughly an
order of magnitude slower than the compiled yajl2_c backend. This was fixed
for this session via, inside the property_tax_project conda env:

    pip install --force-reinstall --no-deps ijson

which pulls the PyPI wheel (bundles the compiled _yajl2 extension) instead
of the conda-forge build. Do NOT add this to environment.yml -- a future
`conda env update -f environment.yml` would silently reinstall the slow
conda-forge build over it. This script checks ijson.backend at startup and
warns loudly if it's not 'yajl2_c'.
"""

import ijson
import json
import pickle
import sys
import time
from datetime import datetime

from scripts.utils import PROJECT_ROOT, format_time, format_size, validate_json_file

JSON_FILE = PROJECT_ROOT / "data" / "sources" / "Travis_protaxExport_20250720.json"
CHECKPOINT_FILE = PROJECT_ROOT / "docs" / "tcad_eda" / "_scan_checkpoint.pkl"
OUTPUT_JSON = PROJECT_ROOT / "docs" / "tcad_eda" / "full_inventory_scan.json"
OUTPUT_MD = PROJECT_ROOT / "docs" / "tcad_eda" / "full_inventory_scan.md"

CHECKPOINT_EVERY = 25_000
PROGRESS_EVERY = 10_000
MAX_EXAMPLES = 3
MAX_ARRAY_LEN_KEYS = 20  # distinct array lengths tracked individually; longer tail bucketed


# ============================================================================
# Accumulator tree
# ============================================================================

def new_node():
    return {
        "dict_visits": 0,
        "list_visits": 0,
        "null_count": 0,
        "scalar_type_counts": {},
        "array_len_counts": {},
        "key_presence": {},
        "json_string_decoded": 0,
        "examples": [],
        "children": {},
        "element": None,
    }


def record_scalar(node, value):
    t = type(value).__name__
    node["scalar_type_counts"][t] = node["scalar_type_counts"].get(t, 0) + 1
    if len(node["examples"]) < MAX_EXAMPLES:
        node["examples"].append(value)


def walk(value, node):
    if value is None:
        node["null_count"] += 1
        return

    if isinstance(value, dict):
        node["dict_visits"] += 1
        kp = node["key_presence"]
        children = node["children"]
        for k, v in value.items():
            kp[k] = kp.get(k, 0) + 1
            child = children.get(k)
            if child is None:
                child = new_node()
                children[k] = child
            walk(v, child)
        return

    if isinstance(value, list):
        node["list_visits"] += 1
        n = len(value)
        alc = node["array_len_counts"]
        key = str(n) if n <= MAX_ARRAY_LEN_KEYS else f">{MAX_ARRAY_LEN_KEYS}"
        alc[key] = alc.get(key, 0) + 1
        if n:
            elem = node["element"]
            if elem is None:
                elem = new_node()
                node["element"] = elem
            for item in value:
                walk(item, elem)
        return

    if isinstance(value, str):
        record_scalar(node, value)
        s = value.strip()
        # Cheap pre-filter before attempting json.loads, so the exception
        # path only gets hit on strings that actually look like JSON.
        if len(s) > 1 and s[0] in "{[" and s[-1] in "}]":
            try:
                decoded = json.loads(s)
            except ValueError:
                decoded = None
            if isinstance(decoded, (dict, list)):
                node["json_string_decoded"] += 1
                jchild = node["children"].get("→json")
                if jchild is None:
                    jchild = new_node()
                    node["children"]["→json"] = jchild
                walk(decoded, jchild)
        return

    record_scalar(node, value)


# ============================================================================
# Flatten + render
# ============================================================================

def flatten(node, path, out):
    total_visits = (
        node["dict_visits"] + node["list_visits"] + node["null_count"]
        + sum(node["scalar_type_counts"].values())
    )
    non_null = total_visits - node["null_count"]

    stats = {
        "total_visits": total_visits,
        "dict_visits": node["dict_visits"],
        "list_visits": node["list_visits"],
        "null_count": node["null_count"],
        "population_rate": round(non_null / total_visits, 4) if total_visits else None,
        "scalar_type_counts": node["scalar_type_counts"],
        "array_len_counts": node["array_len_counts"],
        "json_string_decoded": node["json_string_decoded"],
        "examples": [str(e)[:200] for e in node["examples"]],
    }
    if node["children"]:
        denom = node["dict_visits"] or 1
        stats["child_presence_rate"] = {
            k: round(v / denom, 4) for k, v in sorted(node["key_presence"].items())
        }
    out[path] = stats

    for k, child in sorted(node["children"].items()):
        child_path = f"{path}.{k}" if path else k
        flatten(child, child_path, out)

    if node["element"] is not None:
        elem_path = f"{path}[]"
        flatten(node["element"], elem_path, out)


def render_markdown(flat, meta):
    lines = []
    lines.append("# Full-Population TCAD JSON Inventory Scan\n")
    lines.append(
        f"Generated {meta['scan_date']} by `scripts/inventory_scan_full.py`. "
        f"Scanned {meta['records_scanned']:,} of {meta['records_total_expected']:,} "
        f"top-level parcel records in {format_time(meta['runtime_seconds'])} "
        f"using the `{meta['ijson_backend']}` ijson backend"
        f"{' (resumed run)' if meta['resumed'] else ''}.\n"
    )
    lines.append(
        "This supersedes any 500-record-sample population percentages quoted "
        "in `protax_extraction_structure.md` / `owner_data_structure.md` -- "
        "these numbers are from the full population, not a sample.\n"
    )

    # Group paths by top-level key for readability
    groups = {}
    for path in sorted(flat.keys()):
        top = path.split(".")[0].split("[")[0]
        groups.setdefault(top, []).append(path)

    lines.append("## Fields by top-level array/group\n")
    for top in sorted(groups.keys()):
        if top == "":
            continue
        lines.append(f"### `{top}`\n")
        lines.append("| Path | Population % | Type(s) | Examples |")
        lines.append("|---|---|---|---|")
        for path in groups[top]:
            s = flat[path]
            pop = f"{s['population_rate']*100:.1f}%" if s["population_rate"] is not None else "—"
            types = ", ".join(f"{k}({v})" for k, v in sorted(s["scalar_type_counts"].items())) or "—"
            ex = "; ".join(s["examples"][:2])
            if s["json_string_decoded"]:
                ex += f"  [json-string-decoded x{s['json_string_decoded']}]"
            lines.append(f"| `{path}` | {pop} | {types} | {ex[:150]} |")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# Checkpointing
# ============================================================================

def save_checkpoint(root, records_done):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, "wb") as f:
        pickle.dump({"root": root, "records_done": records_done}, f)


def load_checkpoint():
    with open(CHECKPOINT_FILE, "rb") as f:
        data = pickle.load(f)
    return data["root"], data["records_done"]


# ============================================================================
# Main
# ============================================================================

def run(limit=None, resume=False):
    print("=" * 60)
    print("TCAD Full-Population Inventory Scan")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    if ijson.backend != "yajl2_c":
        print(
            f"\n  WARNING: ijson backend is '{ijson.backend}', not the compiled "
            f"'yajl2_c' backend. This will be roughly an order of magnitude "
            f"slower. Run:\n"
            f"    pip install --force-reinstall --no-deps ijson\n"
            f"  inside the property_tax_project conda env before a full run.\n"
        )

    validate_json_file(JSON_FILE)
    file_size = JSON_FILE.stat().st_size

    resumed = False
    records_done = 0
    root = new_node()

    if resume and CHECKPOINT_FILE.exists():
        print(f"\nResuming from checkpoint: {CHECKPOINT_FILE}")
        root, records_done = load_checkpoint()
        resumed = True
        print(f"  Checkpoint had {records_done:,} records already processed.")

    start_time = time.time()
    n = 0

    try:
        with open(JSON_FILE, "rb") as f:
            parser = ijson.items(f, "item", use_float=True)

            for record in parser:
                n += 1

                if n <= records_done:
                    # Already accounted for in a resumed checkpoint --
                    # ijson can't seek mid-array, so we still pay the parse
                    # cost, but skip the (dominant) Python-side recursion.
                    continue

                walk(record, root)

                if n % CHECKPOINT_EVERY == 0 and limit is None:
                    save_checkpoint(root, n)

                if n % PROGRESS_EVERY == 0:
                    elapsed = time.time() - start_time
                    processed_this_run = n - records_done
                    rate = processed_this_run / elapsed if elapsed > 0 else 0
                    print(
                        f"  {n:,} records | {rate:,.0f}/sec this run | "
                        f"elapsed {format_time(elapsed)}"
                    )

                if limit is not None and n >= limit:
                    break

    except KeyboardInterrupt:
        print("\n\nInterrupted -- saving checkpoint...")
        save_checkpoint(root, n)
        print(f"Checkpoint saved at {n:,} records. Re-run with --resume to continue.")
        return

    elapsed = time.time() - start_time
    processed_this_run = n - records_done
    rate = processed_this_run / elapsed if elapsed > 0 else 0

    print("-" * 60)
    print(f"Processed {n:,} records total ({processed_this_run:,} this run) "
          f"in {format_time(elapsed)} ({rate:,.0f}/sec this run)")

    if limit is not None:
        est_total_seconds = (486_859 / rate) if rate > 0 else float("nan")
        print(f"\nExtrapolated full-population runtime estimate: "
              f"{format_time(est_total_seconds)} (486,859 records @ {rate:,.0f}/sec)")
        print("(Timing-test run -- no output files written.)")
        return

    # Full run complete -- write outputs
    flat = {}
    flatten(root, "", flat)

    meta = {
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "records_scanned": n,
        "records_total_expected": 486_859,
        "runtime_seconds": elapsed,
        "ijson_backend": ijson.backend,
        "resumed": resumed,
        "source_file": str(JSON_FILE),
        "source_file_size": format_size(file_size),
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"_meta": meta, "fields": flat}, f, indent=2, default=str)
    print(f"\nWrote {OUTPUT_JSON}")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(render_markdown(flat, meta))
    print(f"Wrote {OUTPUT_MD}")

    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()
        print(f"Removed checkpoint file (scan complete).")


if __name__ == "__main__":
    limit = None
    resume = False
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
        if arg == "--resume":
            resume = True

    run(limit=limit, resume=resume)
