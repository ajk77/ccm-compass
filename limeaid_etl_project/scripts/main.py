import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.etl.load import load_all_tables
from src.qa.checks import run_integrity_checks
from src.stats.descriptive import compute_summaries
import yaml

config_path = 'config/config.yaml'
chunk_size = 10000

print("Starting full pipeline...")

# ETL
print("Running ETL...")
load_all_tables(config_path, chunk_size)
print("ETL complete.")

# QA
print("Running QA...")
results = run_integrity_checks(config_path)
for table, res in results.items():
    status = "PASS" if res['pass'] else "FAIL"
    print(f"{table}: Null rate = {res['null_rate']:.4f} - {status}")
print("QA complete.")

# Stats
print("Running Stats...")
summaries = compute_summaries(config_path)
output_path = 'data/processed/stats.csv'
summaries.to_csv(output_path)
print(f"Stats saved to {output_path}")
print("Stats complete.")

print("Full pipeline finished successfully.")