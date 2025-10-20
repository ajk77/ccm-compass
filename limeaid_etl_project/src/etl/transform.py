import pandas as pd

def standardize_dtypes(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Standardize data types for specific tables."""
    if table_name == 'MEASUREMENT':
        # Apply user's specified dtypes
        df = df.copy()
        df['value_as_number'] = df['value_as_number'].astype('float64')
        df['value_source_value'] = df['value_source_value'].astype('object')
        df['unit_concept_id'] = df['unit_concept_id'].astype('Int64')  # Nullable integer
    # For other tables, let pandas infer
    return df

def clean_data(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Clean and standardize data."""
    df = standardize_dtypes(df, table_name)
    # Add any other cleaning logic here
    return df