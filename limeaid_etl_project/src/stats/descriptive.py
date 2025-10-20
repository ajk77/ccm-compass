from sqlalchemy import create_engine, inspect, text
import pandas as pd
import yaml
from typing import Dict, Any

def compute_table_stats(engine, table: str, columns: list) -> pd.DataFrame:
    """Compute basic statistics for a table using SQL queries."""
    stats = {}
    
    with engine.connect() as conn:
        total_rows = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
    
    stats['count'] = [total_rows] * len(columns)
    stats['column'] = columns
    
    for col in columns:
        with engine.connect() as conn:
            # Check if column is numeric by trying to get min/max
            try:
                min_val = conn.execute(text(f"SELECT MIN({col}) FROM {table}")).scalar()
                max_val = conn.execute(text(f"SELECT MAX({col}) FROM {table}")).scalar()
                avg_val = conn.execute(text(f"SELECT AVG({col}) FROM {table}")).scalar()
                
                if min_val is not None:
                    stats.setdefault('mean', []).append(avg_val)
                    stats.setdefault('min', []).append(min_val)
                    stats.setdefault('max', []).append(max_val)
                else:
                    stats.setdefault('mean', []).append(None)
                    stats.setdefault('min', []).append(None)
                    stats.setdefault('max', []).append(None)
            except:
                # Non-numeric column
                unique_count = conn.execute(text(f"SELECT COUNT(DISTINCT {col}) FROM {table}")).scalar()
                stats.setdefault('mean', []).append(None)
                stats.setdefault('min', []).append(None)
                stats.setdefault('max', []).append(unique_count)  # Use unique count as max for categorical
    
    df = pd.DataFrame(stats)
    df['table'] = table
    return df.set_index(['table', 'column'])

def compute_summaries(config_path: str) -> pd.DataFrame:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    engine = create_engine(f'sqlite:///{config["db_path"]}')
    inspector = inspect(engine)
    
    all_stats = []
    for table in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns(table)]
        table_stats = compute_table_stats(engine, table, columns)
        all_stats.append(table_stats)
    
    return pd.concat(all_stats)