"""
Pipeline Entry Point for Motor Insurance Claims & Policy Analytics.

Orchestrates the complete data engineering flow:
  1. Data Loading: load_all_data()
  2. Data Validation: validate_all_tables()
  3. Data Cleaning & Feature Engineering: clean_data()
  4. Exporting Cleaned Data: save_cleaned_data()
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.logger import setup_logger, log_pipeline_step, log_error
from src.data_loader import load_all_data
from src.validation import validate_all_tables
from src.data_cleaner import clean_data, save_cleaned_data


def run_pipeline(raw_data_dir: str = "data/raw", cleaned_data_dir: str = "data/cleaned") -> dict:
    """
    Executes the motor insurance analytics data pipeline end-to-end.

    Args:
        raw_data_dir: Directory containing raw CSV tables.
        cleaned_data_dir: Destination directory for cleaned tables.

    Returns:
        Dictionary of cleaned DataFrames.

    Raises:
        RuntimeError: If data validation fails.
    """
    setup_logger()
    log_pipeline_step("=" * 60)
    log_pipeline_step("STARTING MOTOR INSURANCE DATA PIPELINE EXECUTION")
    log_pipeline_step("=" * 60)

    # 1. Load data
    raw_path = os.path.join(PROJECT_ROOT, raw_data_dir)
    data = load_all_data(raw_path)

    # 2. Validate tables & relationships
    is_valid = validate_all_tables(data)
    if not is_valid:
        err_msg = "Data validation checks failed! Pipeline execution halted."
        log_error(err_msg)
        raise RuntimeError(err_msg)

    # 3. Clean data & create derived features
    cleaned_data = clean_data(data)

    # 4. Save cleaned tables
    cleaned_path = os.path.join(PROJECT_ROOT, cleaned_data_dir)
    save_cleaned_data(cleaned_data, cleaned_path)

    log_pipeline_step("=" * 60)
    log_pipeline_step("MOTOR INSURANCE DATA PIPELINE COMPLETED SUCCESSFULLY")
    log_pipeline_step("=" * 60)

    return cleaned_data


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        log_error(f"Pipeline execution encountered critical error: {e}")
        sys.exit(1)
