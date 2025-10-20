from sqlalchemy import create_engine
import yaml
from .extract import get_file_groups, read_table_chunks
from .transform import clean_data

def init_db(config_path: str):
    """Initialize the database engine."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    engine = create_engine(f'sqlite:///{config["db_path"]}')
    return engine

def load_table_chunked(table_name: str, file_group, engine, config_path: str, chunk_size: int = 10000):
    """Load a table in chunks."""
    first_chunk = True
    for chunk in read_table_chunks(table_name, file_group, chunk_size):
        cleaned_chunk = clean_data(chunk, table_name)
        if_exists = 'replace' if first_chunk else 'append'
        cleaned_chunk.to_sql(table_name, engine, if_exists=if_exists, index=False)
        first_chunk = False
        print(f"Loaded chunk of {len(cleaned_chunk)} rows into {table_name}")

def load_all_tables(config_path: str, chunk_size: int = 10000):
    """Load all tables into the database."""
    file_groups = get_file_groups(config_path)
    engine = init_db(config_path)
    
    for table_name, file_group in file_groups.items():
        print(f"Loading table: {table_name}")
        load_table_chunked(table_name, file_group, engine, config_path, chunk_size)
        print(f"Finished loading {table_name}")
    
    print("All tables loaded successfully")