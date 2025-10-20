import pandas as pd
import os
from pathlib import Path
import yaml

def analyze_csv_files(config_path='config/config.yaml'):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    raw_dir = Path(config['data_dir'])
    files = list(raw_dir.glob('*.csv'))

    print('Files found:')
    for f in files:
        print(f.name)

    print('\nAnalyzing schemas (first 5 rows):')
    schemas = {}
    for f in files:
        try:
            # Read in chunks if large, but for schema, just first chunk
            df = pd.read_csv(f, nrows=5)
            print(f'\n{f.name}:')
            print('Columns:', list(df.columns))
            print('Dtypes:')
            print(df.dtypes)
            print('Shape (sample):', df.shape)
            schemas[f.stem] = {
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'sample_shape': df.shape
            }
        except Exception as e:
            print(f'Error reading {f.name}: {e}')

    # Identify part1/part2 files
    part_files = {}
    for name in schemas.keys():
        if '_part1' in name or '_part2' in name:
            base = name.replace('_part1', '').replace('_part2', '')
            if base not in part_files:
                part_files[base] = []
            part_files[base].append(name)

    print('\nPart files to combine:')
    for base, parts in part_files.items():
        print(f'{base}: {parts}')
        # Check if schemas match
        if len(parts) == 2:
            cols1 = schemas[parts[0]]['columns']
            cols2 = schemas[parts[1]]['columns']
            if cols1 == cols2:
                print(f'  Schemas match: {len(cols1)} columns')
            else:
                print(f'  Schemas differ: {len(cols1)} vs {len(cols2)} columns')
                print(f'  Cols1: {cols1}')
                print(f'  Cols2: {cols2}')

    return schemas, part_files

if __name__ == '__main__':
    analyze_csv_files()