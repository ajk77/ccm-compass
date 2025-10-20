import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.stats.descriptive import compute_summaries
import yaml

config_path = 'config/config.yaml'
summaries = compute_summaries(config_path)

# Save to CSV
output_path = 'data/processed/stats.csv'
summaries.to_csv(output_path)
print(f"Descriptive statistics saved to {output_path}")

print("Summary of summaries:")
print(summaries.head())