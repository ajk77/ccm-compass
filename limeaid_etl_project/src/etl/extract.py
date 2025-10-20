import pandas as pd
import yaml
from pathlib import Path
from typing import Dict, List, Union

def get_file_groups(config_path: str) -> Dict[str, Union[str, List[str]]]:
    """Get file groups, combining part1/part2 into lists."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    data_dir = Path(config['data_dir'])
    
    files = {f.stem: str(f) for f in data_dir.glob('*.csv')}
    
    # Group part files
    grouped = {}
    for name, path in files.items():
        if '_part1' in name or '_part2' in name:
            base = name.replace('_part1', '').replace('_part2', '')
            if base not in grouped:
                grouped[base] = []
            grouped[base].append(path)
        else:
            grouped[name] = path
    
    return grouped

def read_csv_chunked(file_path: str, chunk_size: int = 10000):
    """Generator to read CSV in chunks."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk

def read_table_chunks(table_name: str, file_group: Union[str, List[str]], chunk_size: int = 10000):
    """Generator to read chunks for a table, combining parts if needed."""
    if isinstance(file_group, list):
        # Multiple parts - yield combined chunks
        iterators = [read_csv_chunked(f, chunk_size) for f in file_group]
        while True:
            chunks = []
            for it in iterators:
                try:
                    chunks.append(next(it))
                except StopIteration:
                    return  # If any iterator is done, stop
            # Combine chunks from all parts
            combined = pd.concat(chunks, ignore_index=True)
            yield combined
    else:
        # Single file
        yield from read_csv_chunked(file_group, chunk_size)