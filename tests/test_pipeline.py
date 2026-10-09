"""
Unit tests for data pipeline and cleaner modules (tests/test_pipeline.py).

Verifies loading, duplicate removal, derived column creation, cleaning pipeline, and saving.
"""

import unittest
import tempfile
import shutil
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_all_data, load_table
from src.data_cleaner import (
    remove_duplicates,
    create_derived_columns,
    clean_data,
    save_cleaned_data
)


class TestPipeline(unittest.TestCase):
    """Test suite for pipeline functions."""

    def setUp(self):
        """Creates small controlled fixtures for pipeline tests."""
        self.customers_df = pd.DataFrame({
            "customer_id": ["C1", "C2", "C1"],  # Duplicate row/PK
            "customer_name": ["Alice ", "Bob", "Alice"],
            "gender": ["F", "M", "F"],
            "date_of_birth": ["1990-01-01", "1985-05-15", "1990-01-01"],
            "age": [36, 41, 36],
            "city": ["Mumbai", "Delhi", "Mumbai"],
            "state": ["Maharashtra", "Delhi", "Maharashtra"],
            "occupation": ["Engineer", "Doctor", "Engineer"]
        })

        self.vehicles_df = pd.DataFrame({
            "vehicle_id": ["V1", "V2"],
            "customer_id": ["C1", "C2"],
            "vehicle_type": ["Car", "Car"],
            "vehicle_make": ["Maruti Suzuki", "Hyundai"],
            "vehicle_model": ["Swift", "i20"],
            "vehicle_year": [2020, 2022],
            "fuel_type": ["Petrol", "Diesel"],
            "vehicle_value": [600000.0, 800000.0]
        })

        self.policies_df = pd.DataFrame({
            "policy_id": ["P1", "P2"],
            "customer_id": ["C1", "C2"],
            "vehicle_id": ["V1", "V2"],
            "policy_start_date": ["2025-01-01", "2025-02-01"],
            "policy_end_date": ["2026-01-01", "2026-02-01"],
            "policy_type": ["Comprehensive", "Third Party"],
            "premium_amount": [20000.0, 10000.0],
            "coverage_amount": [500000.0, 300000.0],
            "policy_status": ["Active", "Expired"],
            "payment_frequency": ["Annual", "Semi-Annual"]
        })

        self.claims_df = pd.DataFrame({
            "claim_id": ["CLM1", "CLM2"],
            "policy_id": ["P1", "P2"],
            "customer_id": ["C1", "C2"],
            "claim_date": ["2025-06-15", "2025-07-20"],
            "accident_date": ["2025-06-10", "2025-07-18"],
            "claim_type": ["Accident", "Theft"],
            "accident_location": ["City Road", "Parking Area"],
            "claim_amount": [40000.0, 80000.0],
            "claim_status": ["Approved", "Settled"],
            "approval_date": ["2025-06-25", "2025-07-25"],
            "settlement_date": [None, "2025-08-05"],
            "damage_severity": ["Medium", "High"]
        })

        self.payments_df = pd.DataFrame({
            "payment_id": ["PAY1"],
            "claim_id": ["CLM2"],
            "policy_id": ["P2"],
            "payment_date": ["2025-08-05"],
            "payment_amount": [75000.0],
            "payment_status": ["Completed"],
            "payment_method": ["Bank Transfer"]
        })

        self.test_data = {
            "customers": self.customers_df,
            "vehicles": self.vehicles_df,
            "policies": self.policies_df,
            "claims": self.claims_df,
            "payments": self.payments_df
        }

    def test_load_all_data(self):
        """Proves load_all_data accurately loads all 5 tables from a directory."""
        # Test loading from cleaned dataset directory
        cleaned_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "cleaned"))
        data = load_all_data(cleaned_dir)
        self.assertIn("customers", data)
        self.assertIn("vehicles", data)
        self.assertIn("policies", data)
        self.assertIn("claims", data)
        self.assertIn("payments", data)
        self.assertEqual(len(data["policies"]), 25000)
        self.assertEqual(len(data["claims"]), 10000)

    def test_remove_duplicates(self):
        """Proves remove_duplicates detects and removes duplicate primary keys and duplicate rows."""
        self.assertEqual(len(self.test_data["customers"]), 3)
        deduped = remove_duplicates(self.test_data)
        # Duplicate C1 row should be eliminated
        self.assertEqual(len(deduped["customers"]), 2)
        self.assertEqual(deduped["customers"]["customer_id"].tolist(), ["C1", "C2"])

    def test_create_derived_columns(self):
        """Proves create_derived_columns generates all required insurance metrics."""
        derived = create_derived_columns(self.test_data)

        # Check policies derived fields
        self.assertIn("policy_duration_days", derived["policies"].columns)
        self.assertIn("policy_active_flag", derived["policies"].columns)
        self.assertEqual(derived["policies"]["policy_active_flag"].tolist(), [1, 0])

        # Check vehicles derived fields
        self.assertIn("vehicle_age", derived["vehicles"].columns)

        # Check claims derived fields
        self.assertIn("claim_processing_days", derived["claims"].columns)
        self.assertIn("claim_settlement_days", derived["claims"].columns)
        self.assertIn("claim_to_premium_ratio", derived["claims"].columns)
        self.assertIn("claim_to_coverage_ratio", derived["claims"].columns)
        self.assertIn("paid_claim_ratio", derived["claims"].columns)

    def test_clean_data(self):
        """Proves clean_data executes the sequential cleaning pipeline without data corruption."""
        cleaned = clean_data(self.test_data)
        self.assertEqual(len(cleaned["customers"]), 2)  # duplicates removed
        self.assertIn("policy_duration_days", cleaned["policies"].columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned["policies"]["policy_start_date"]))

    def test_save_cleaned_data(self):
        """Proves save_cleaned_data writes all 5 expected CSV files to destination directory."""
        temp_dir = tempfile.mkdtemp()
        try:
            save_cleaned_data(self.test_data, temp_dir)
            expected_files = [
                "customers_cleaned.csv",
                "vehicles_cleaned.csv",
                "policies_cleaned.csv",
                "claims_cleaned.csv",
                "payments_cleaned.csv"
            ]
            for ef in expected_files:
                target = os.path.join(temp_dir, ef)
                self.assertTrue(os.path.isfile(target), f"File {ef} was not created.")
                df_loaded = pd.read_csv(target)
                self.assertFalse(df_loaded.empty)
        finally:
            shutil.rmtree(temp_dir)


# Standalone function wrappers for pytest compatibility
def test_load_all_data():
    tc = TestPipeline()
    tc.setUp()
    tc.test_load_all_data()

def test_remove_duplicates():
    tc = TestPipeline()
    tc.setUp()
    tc.test_remove_duplicates()

def test_create_derived_columns():
    tc = TestPipeline()
    tc.setUp()
    tc.test_create_derived_columns()

def test_clean_data():
    tc = TestPipeline()
    tc.setUp()
    tc.test_clean_data()

def test_save_cleaned_data():
    tc = TestPipeline()
    tc.setUp()
    tc.test_save_cleaned_data()


if __name__ == "__main__":
    unittest.main()
