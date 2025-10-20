import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.etl.load import load_all_tables

config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
chunk_size = 10000

print("Starting ETL pipeline...")
load_all_tables(str(config_path), chunk_size)
print("ETL complete.")