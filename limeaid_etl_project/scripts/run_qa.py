import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.qa.checks import run_integrity_checks
import yaml

config_path = 'config/config.yaml'
results = run_integrity_checks(config_path)

print("QA Results:")
for table, res in results.items():
    status = "PASS" if res['pass'] else "FAIL"
    print(f"{table}: Null rate = {res['null_rate']:.4f} - {status}")

# Load thresholds
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
threshold = config['qa_thresholds']['null_rate_max']
print(f"\nThreshold: null_rate_max = {threshold}")