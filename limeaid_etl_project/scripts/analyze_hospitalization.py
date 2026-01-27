import pandas as pd
import os
from pathlib import Path
import yaml
from datetime import datetime

def analyze_hospitalization(config_path='config/config.yaml'):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    raw_dir = Path(config['data_dir'])
    processed_dir = Path(config['processed_dir'])
    file_path = raw_dir / 'HOSPITALIZATION_COMPASS.csv'

    if not file_path.exists():
        print(f"File {file_path} not found.")
        return

    # Load the data
    df = pd.read_csv(file_path)

    # Calculate unique counts
    unique_counts = {
        'person_id': df['person_id'].nunique(),
        'visit_occurrence_id': df['visit_occurrence_id'].nunique(),
        'flag_includes_nicu_admit': df['flag_includes_nicu_admit'].nunique(),
        'flag_includes_icu_admit': df['flag_includes_icu_admit'].nunique()
    }

    print("Unique Counts:")
    for col, count in unique_counts.items():
        print(f"{col}: {count}")

    # Group by unique values and count
    group_cols = ['location_id', 'gender_concept_id', 'race_concept_id', 'ethnicity_concept_id',
                  'visit_concept_id', 'admitted_from_concept_id', 'discharged_to_concept_id', 'payer_concept_id']
    grouped = df.groupby(group_cols).size().reset_index(name='count')
    grouped_file = processed_dir / 'hospitalization_grouped_new.csv'
    grouped.to_csv(grouped_file, index=False)
    print(f"\nGrouped counts saved to {grouped_file}")

    # Calculate length_of_stay in days
    df['visit_start_datetime'] = pd.to_datetime(df['visit_start_datetime'])
    df['visit_end_datetime'] = pd.to_datetime(df['visit_end_datetime'])
    df['length_of_stay_days'] = (df['visit_end_datetime'] - df['visit_start_datetime']).dt.total_seconds() / (60*60*24)

    # Calculate quartiles
    quartiles = {}
    for col in ['age_at_admit', 'length_of_stay_days', 'icu_los_hours']:
        quartiles[col] = df[col].quantile([0.25, 0.5, 0.75, 1.0]).to_dict()

    print("\nQuartiles:")
    for col, quarts in quartiles.items():
        print(f"{col}: {quarts}")

    # Save quartiles to file
    quartiles_df = pd.DataFrame(quartiles)
    quartiles_file = processed_dir / 'hospitalization_quartiles.csv'
    quartiles_df.to_csv(quartiles_file)
    print(f"Quartiles saved to {quartiles_file}")

if __name__ == "__main__":
    analyze_hospitalization()