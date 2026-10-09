"""
Data loader module for Motor Insurance Claims & Policy Analytics.

Responsible for checking file existence, loading individual CSV tables,
and batch-loading all related insurance tables with robust error handling and logging.
Supports loading both raw ('customers.csv') and cleaned ('customers_cleaned.csv') naming schemes.
"""

import os
from typing import Dict
import pandas as pd
from src.logger import log_pipeline_step, log_error

TABLE_NAMES = [
    "customers",
    "vehicles",
    "policies",
    "claims",
    "payments"
]


def check_file_exists(file_path: str) -> bool:
    """
    Checks if a file exists at the specified path.

    Args:
        file_path: Relative or absolute path to the file.

    Returns:
        True if the file exists and is a regular file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        err_msg = f"Required file not found: {file_path}"
        log_error(err_msg)
        raise FileNotFoundError(err_msg)
    return True


def load_table(file_path: str) -> pd.DataFrame:
    """
    Loads a single CSV table into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file to load.

    Returns:
        DataFrame containing the loaded table data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If loading fails or file is empty.
    """
    check_file_exists(file_path)
    try:
        df = pd.read_csv(file_path)
        log_pipeline_step(f"Loaded table '{os.path.basename(file_path)}' with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        err_msg = f"Failed to load table from {file_path}: {str(e)}"
        log_error(err_msg)
        raise ValueError(err_msg) from e


def load_all_data(data_dir: str) -> Dict[str, pd.DataFrame]:
    """
    Loads all required motor insurance tables from the specified directory.
    Seamlessly resolves both standard ('table.csv') and cleaned ('table_cleaned.csv') files.

    Expected tables:
      - customers
      - vehicles
      - policies
      - claims
      - payments

    Args:
        data_dir: Path to directory containing raw or cleaned CSV files.

    Returns:
        Dictionary mapping table names ('customers', 'vehicles', 'policies',
        'claims', 'payments') to their respective DataFrames.

    Raises:
        FileNotFoundError: If any required table is missing.
    """
    log_pipeline_step(f"Initiating batch data loading from directory: '{data_dir}'")
    if not os.path.isdir(data_dir):
        err_msg = f"Specified data directory does not exist: {data_dir}"
        log_error(err_msg)
        raise FileNotFoundError(err_msg)

    data = {}
    for table in TABLE_NAMES:
        standard_path = os.path.join(data_dir, f"{table}.csv")
        cleaned_path = os.path.join(data_dir, f"{table}_cleaned.csv")

        if os.path.isfile(standard_path):
            target_path = standard_path
        elif os.path.isfile(cleaned_path):
            target_path = cleaned_path
        else:
            err_msg = f"Required table '{table}' not found as '{table}.csv' or '{table}_cleaned.csv' in '{data_dir}'."
            log_error(err_msg)
            raise FileNotFoundError(err_msg)

        data[table] = load_table(target_path)

    log_pipeline_step("Successfully loaded all related insurance tables.")
    return data
