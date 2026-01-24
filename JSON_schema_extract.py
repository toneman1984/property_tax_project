import json
import sqlite3
from collections import defaultdict
from typing import Any, Dict, Set
from decimal import Decimal
from pathlib import Path

def decimal_default(obj):
    """Convert Decimal objects to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def insert_batch(cursor, table_name: str, columns: list, batch: list):
    """Insert a batch of records."""
    placeholders = ','.join(['?' for _ in columns])
    sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
    
    rows = []
    for record in batch:
        row = []
        for col in columns:
            # Handle sanitized column names
            value = None
            
            # Try to find matching key in record
            for key in record.keys():
                sanitized_key = key.replace(' ', '_').replace('-', '_').replace('.', '_')
                sanitized_key = ''.join(c if c.isalnum() or c == '_' else '_' for c in sanitized_key)
                if sanitized_key == col:
                    value = record[key]
                    break
            
            # Handle different value types
            if value is None:
                row.append(None)
            elif isinstance(value, Decimal):
                # Convert Decimal to float or int
                row.append(float(value) if value % 1 else int(value))
            elif isinstance(value, (dict, list)):
                # Convert complex types to JSON strings, handling Decimals
                try:
                    row.append(json.dumps(value, default=decimal_default))
                except (TypeError, ValueError) as e:
                    print(f"Warning: Could not serialize value for column {col}: {e}")
                    row.append(str(value))
            else:
                row.append(value)
        rows.append(tuple(row))
    
    cursor.executemany(sql, rows)

def analyze_record(record: Dict[str, Any], schema: Dict[str, Set[type]], prefix: str = ""):
    """Recursively analyze a record and update schema."""
    if isinstance(record, dict):
        for key, value in record.items():
            full_key = f"{prefix}{key}" if not prefix else f"{prefix}_{key}"
            
            if value is None:
                schema[full_key].add(type(None))
            elif isinstance(value, Decimal):
                # Treat Decimal as float
                schema[full_key].add(float)
            elif isinstance(value, bool):  # Check bool before int (bool is subclass of int)
                schema[full_key].add(bool)
            elif isinstance(value, int):
                schema[full_key].add(int)
            elif isinstance(value, float):
                schema[full_key].add(float)
            elif isinstance(value, str):
                schema[full_key].add(str)
            elif isinstance(value, (list, dict)):
                # Store complex types as JSON TEXT in SQLite
                schema[full_key].add(str)  # Will store as JSON string

def infer_schema_with_ijson(json_file_path: str, sample_size: int = 1000):
    """
    Use ijson for streaming JSON parsing - works with any valid JSON format.
    """
    import ijson
    schema = defaultdict(set)
    records_processed = 0
    
    try:
        with open(json_file_path, 'rb') as f:
            # Try to parse as array of objects
            parser = ijson.items(f, 'item')
            for record in parser:
                if records_processed >= sample_size:
                    break
                if isinstance(record, dict):
                    analyze_record(record, schema)
                    records_processed += 1
                    if records_processed % 100 == 0:
                        print(f"Processed {records_processed} records...")
    except ijson.JSONError:
        # If that fails, try parsing the entire structure
        print("Trying alternative parsing method...")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    for record in data[:sample_size]:
                        if isinstance(record, dict):
                            analyze_record(record, schema)
                            records_processed += 1
                elif isinstance(data, dict):
                    # Single object or nested structure
                    analyze_record(data, schema)
                    records_processed = 1
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
    
    return schema, records_processed

def python_type_to_sqlite(types: Set[type]) -> str:
    """Convert Python types to SQLite types."""
    types.discard(type(None))  # Remove None from consideration
    
    if not types:
        return "TEXT"
    
    # If multiple types, prioritize TEXT for flexibility
    if len(types) > 1:
        if float in types:
            return "REAL"
        if int in types and bool not in types:
            return "INTEGER"
        return "TEXT"
    
    type_map = {
        int: "INTEGER",
        float: "REAL",
        str: "TEXT",
        bool: "INTEGER",  # SQLite stores booleans as 0/1
    }
    
    return type_map.get(list(types)[0], "TEXT")

def create_table_schema(schema: Dict[str, Set[type]], table_name: str = "data") -> str:
    """Generate CREATE TABLE SQL statement."""
    if not schema:
        raise ValueError("No schema detected. Please check your JSON file format.")
    
    columns = []
    
    for column_name, types in sorted(schema.items()):
        sql_type = python_type_to_sqlite(types)
        # Sanitize column name (replace spaces, special chars)
        safe_column_name = column_name.replace(' ', '_').replace('-', '_').replace('.', '_')
        safe_column_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in safe_column_name)
        columns.append(f"    {safe_column_name} {sql_type}")
    
    create_statement = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    create_statement += ",\n".join(columns)
    create_statement += "\n);"
    
    return create_statement

def insert_data_with_ijson(json_file_path: str, db_path: str, table_name: str = "data", 
                           batch_size: int = 1000):
    """
    Stream JSON data using ijson and insert into SQLite in batches.
    """
    import ijson
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Optimize SQLite for bulk inserts
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA cache_size = 10000")
    
    # Get column names from table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    
    batch = []
    total_inserted = 0
    
    try:
        with open(json_file_path, 'rb') as f:
            parser = ijson.items(f, 'item')
            for record in parser:
                if isinstance(record, dict):
                    batch.append(record)
                    
                    if len(batch) >= batch_size:
                        insert_batch(cursor, table_name, columns, batch)
                        total_inserted += len(batch)
                        batch = []
                        conn.commit()
                        print(f"Inserted {total_inserted} records...")
    except ijson.JSONError:
        # Fallback to standard JSON loading
        print("Using fallback insertion method...")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for record in data:
                    if isinstance(record, dict):
                        batch.append(record)
                        
                        if len(batch) >= batch_size:
                            insert_batch(cursor, table_name, columns, batch)
                            total_inserted += len(batch)
                            batch = []
                            conn.commit()
                            print(f"Inserted {total_inserted} records...")
    
    # Insert remaining records
    if batch:
        insert_batch(cursor, table_name, columns, batch)
        total_inserted += len(batch)
    
    conn.commit()
    conn.close()
    print(f"Total records inserted: {total_inserted}")

# Example usage
if __name__ == "__main__":
    # Define paths relative to project root
    PROJECT_ROOT = Path(__file__).parent
    DATA_RAW = PROJECT_ROOT / "data" / "raw"
    DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

    # Create data directories if they don't exist
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    # Input/output files (update json_filename as needed)
    json_filename = "Travis_protaxExport_20250720.json"
    json_file = DATA_RAW / json_filename
    db_file = DATA_PROCESSED / json_filename.replace(".json", ".db")

    # Check that input file exists
    if not json_file.exists():
        print(f"ERROR: Input file not found: {json_file}")
        print(f"Please place your JSON file in: {DATA_RAW}")
        exit(1)

    # First, let's inspect the file
    print("Inspecting JSON file...")
    with open(json_file, 'r', encoding='utf-8') as f:
        first_lines = [f.readline() for _ in range(5)]
        print("First few lines:")
        for i, line in enumerate(first_lines, 1):
            print(f"Line {i}: {line[:100]}...")
    
    print("\n" + "="*50)
    
    # Step 1: Infer schema from sample
    print("\nAnalyzing JSON structure...")
    
    # Try ijson first
    try:
        import ijson
        schema, sample_count = infer_schema_with_ijson(json_file, sample_size=1000)
    except ImportError:
        print("ijson not installed")
        print("Install with: pip install ijson")
        exit(1)
    
    print(f"\nAnalyzed {sample_count} records")
    
    if not schema:
        print("\nERROR: Could not detect any schema from the JSON file.")
        exit(1)
    
    print("\nDetected schema:")
    for column, types in sorted(schema.items()):
        type_names = [t.__name__ for t in types]
        print(f"  {column}: {', '.join(type_names)}")
    
    # Step 2: Create table
    print("\nGenerating CREATE TABLE statement...")
    create_sql = create_table_schema(schema, "my_table")
    print(create_sql)
    
    # Step 3: Create database and table
    conn = sqlite3.connect(db_file)
    conn.execute(create_sql)
    conn.close()
    print(f"\nTable created in {db_file}")
    
    # Step 4: Insert data
    print("\nInserting data...")
    insert_data_with_ijson(json_file, db_file, "my_table", batch_size=1000)
    
    print("\nDone!")
    
    # Show summary
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM my_table")
    count = cursor.fetchone()[0]
    print(f"\nTotal records in database: {count}")
    conn.close()