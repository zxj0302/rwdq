import sqlite3
import json
import torch
import io
import math
import argparse

def load_config_from_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def query_database(db_file, config):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    where_clauses = []
    for attr, bounds in config.items():
        if attr in ['domain', 'limit']:
            continue
        lower = bounds.get('min', 0)
        upper = bounds.get('max', math.inf)

        if lower == 0 and upper == math.inf:
            continue
        elif lower == 0:
            where_clauses.append(f"{attr} <= {upper}")
        elif upper == math.inf:
            where_clauses.append(f"{attr} >= {lower}")
        else:
            where_clauses.append(f"{attr} BETWEEN {lower} AND {upper}")

    if 'domain' in config:
        domain_values = ", ".join(f"'{d}'" for d in config['domain'])
        where_clauses.append(f"domain IN ({domain_values})")

    where_statement = " AND ".join(where_clauses)

    query = f"SELECT data FROM rwd WHERE {where_statement} ORDER BY RANDOM()"

    if 'limit' in config:
        query += f" LIMIT {config['limit']}"

    print("Executing SQL query:\n")
    print(query, "\n")

    cursor.execute(f"SELECT COUNT(*) FROM rwd WHERE {where_statement}")
    total_count = cursor.fetchone()[0]

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    return results, total_count

def binary_to_data(binary):
    buffer = io.BytesIO(binary)
    return torch.load(buffer)

def run_query(config_file, db_file, output_file):
    config = load_config_from_json(config_file)
    results, total_count = query_database(db_file, config)

    data_objects = [binary_to_data(row[0]) for row in results]

    print(f"Retrieved Data objects: {len(data_objects)}/{total_count}\n")

    print("Example Data Object:\n")
    if data_objects:
        print(data_objects[0], "\n")

    # Save the data objects to a file
    if output_file is not None:
        torch.save(data_objects, output_file)
        print(f"Data objects saved to {output_file}")

    return data_objects

def main():
    parser = argparse.ArgumentParser(description="Query a database based on configuration.")
    parser.add_argument('--config', default='config.json', help='Path to the configuration JSON file (default: config.json)')
    parser.add_argument('--database', default='rwd.db', help='Path to the SQLite database file (default: rwd.db)')
    parser.add_argument('--output', default=None, help='Path to the output file (default: None)')
    args = parser.parse_args()

    run_query(args.config, args.database, args.output)

if __name__ == "__main__":
    main()