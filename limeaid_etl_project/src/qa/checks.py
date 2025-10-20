from sqlalchemy import create_engine, inspect, text
import pandas as pd
import yaml

def run_integrity_checks(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    engine = create_engine(f'sqlite:///{config["db_path"]}')
    inspector = inspect(engine)
    results = {}
    for table in inspector.get_table_names():
        # Get column names
        columns = inspector.get_columns(table)
        col_names = [col['name'] for col in columns]
        
        # Get total row count
        with engine.connect() as conn:
            total_rows = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        
        if total_rows == 0:
            results[table] = {'null_rate': 0.0, 'pass': True}
            continue
        
        # Calculate null rates using SQL
        null_counts = []
        with engine.connect() as conn:
            for col in col_names:
                null_count = conn.execute(text(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")).scalar()
                null_counts.append(null_count)
        
        avg_null_rate = sum(null_counts) / (len(col_names) * total_rows)
        results[table] = {'null_rate': avg_null_rate, 'pass': avg_null_rate < config['qa_thresholds']['null_rate_max']}
    return results