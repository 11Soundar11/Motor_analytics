"""
Unit tests for validation module (tests/test_validation.py).

Verifies expected behavior of validation functions on small controlled DataFrames.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.validation import (
    validate_customers,
    validate_policies,
    validate_claims,
    validate_relationships
)


class TestValidation(unittest.TestCase):
    """Test suite for validation functions."""

    def setUp(self):
        """Set up small controlled DataFrames for testing."""
        self.customers_df = pd.DataFrame({
            "customer_id": ["C1", "C2", "C3"],
            "customer_name": ["Alice", "Bob", "Charlie"],
            "gender": ["F", "M", "M"],
            "date_of_birth": ["1990-01-01", "1985-05-15", "2000-10-20"],
            "age": [36, 41, 26],
            "city": ["Mumbai", "Delhi", "Bengaluru"],
            "state": ["Maharashtra", "Delhi", "Karnataka"],
            "occupation": ["Engineer", "Doctor", "Teacher"]
        })

        self.vehicles_df = pd.DataFrame({
            "vehicle_id": ["V1", "V2", "V3"],
            "customer_id": ["C1", "C2", "C3"],
            "vehicle_type": ["Car", "Car", "Car"],
            "vehicle_make": ["Maruti Suzuki", "Hyundai", "Tata"],
            "vehicle_model": ["Swift", "i20", "Nexon"],
            "vehicle_year": [2020, 2021, 2022],
            "fuel_type": ["Petrol", "Diesel", "Electric"],
            "vehicle_value": [600000.0, 800000.0, 1200000.0]
        })

        self.policies_df = pd.DataFrame({
            "policy_id": ["P1", "P2", "P3"],
            "customer_id": ["C1", "C2", "C3"],
            "vehicle_id": ["V1", "V2", "V3"],
            "policy_start_date": ["2025-01-01", "2025-02-01", "2025-03-01"],
            "policy_end_date": ["2026-01-01", "2026-02-01", "2026-03-01"],
            "policy_type": ["Comprehensive", "Third Party", "Zero Depreciation"],
            "premium_amount": [25000.0, 15000.0, 32000.0],
            "coverage_amount": [500000.0, 300000.0, 800000.0],
            "policy_status": ["Active", "Expired", "Renewed"],
            "payment_frequency": ["Annual", "Semi-Annual", "Annual"]
        })

        self.claims_df = pd.DataFrame({
            "claim_id": ["CLM1", "CLM2"],
            "policy_id": ["P1", "P3"],
            "customer_id": ["C1", "C3"],
            "claim_date": ["2025-06-15", "2025-07-20"],
            "accident_date": ["2025-06-10", "2025-07-18"],
            "claim_type": ["Accident", "Theft"],
            "accident_location": ["City Road", "Parking Area"],
            "claim_amount": [45000.0, 120000.0],
            "claim_status": ["Approved", "Settled"],
            "approval_date": ["2025-06-25", "2025-07-25"],
            "settlement_date": [None, "2025-08-05"],
            "damage_severity": ["Medium", "High"]
        })

        self.payments_df = pd.DataFrame({
            "payment_id": ["PAY1"],
            "claim_id": ["CLM2"],
            "policy_id": ["P3"],
            "payment_date": ["2025-08-05"],
            "payment_amount": [115000.0],
            "payment_status": ["Completed"],
            "payment_method": ["Bank Transfer"]
        })

    def test_validate_customers(self):
        """Proves validate_customers passes valid customer tables and catches missing columns/duplicates."""
        self.assertTrue(validate_customers(self.customers_df))

        # Check duplicate primary key failure
        dup_df = self.customers_df.copy()
        dup_df.loc[2, "customer_id"] = "C1"
        self.assertFalse(validate_customers(dup_df))

        # Check missing required column
        missing_df = self.customers_df.drop(columns=["age"])
        self.assertFalse(validate_customers(missing_df))

    def test_validate_policies(self):
        """Proves validate_policies checks schema, amounts, and categorical constraints."""
        self.assertTrue(validate_policies(self.policies_df))

        # Check negative premium
        neg_df = self.policies_df.copy()
        neg_df.loc[0, "premium_amount"] = -500.0
        self.assertFalse(validate_policies(neg_df))

        # Check invalid status
        inv_status_df = self.policies_df.copy()
        inv_status_df.loc[0, "policy_status"] = "InvalidStatus"
        self.assertFalse(validate_policies(inv_status_df))

    def test_validate_claims(self):
        """Proves validate_claims enforces schema, positive amounts, and allowed statuses."""
        self.assertTrue(validate_claims(self.claims_df))

        # Check negative claim amount
        neg_clm = self.claims_df.copy()
        neg_clm.loc[0, "claim_amount"] = -100.0
        self.assertFalse(validate_claims(neg_clm))

        # Check invalid severity
        inv_sev = self.claims_df.copy()
        inv_sev.loc[0, "damage_severity"] = "Catastrophic"
        self.assertFalse(validate_claims(inv_sev))

    def test_validate_relationships(self):
        """Proves validate_relationships checks foreign key integrity across related tables."""
        data = {
            "customers": self.customers_df,
            "vehicles": self.vehicles_df,
            "policies": self.policies_df,
            "claims": self.claims_df,
            "payments": self.payments_df
        }
        self.assertTrue(validate_relationships(data))

        # Introduce broken foreign key
        broken_claims = self.claims_df.copy()
        broken_claims.loc[0, "policy_id"] = "POL_NON_EXISTENT"
        bad_data = data.copy()
        bad_data["claims"] = broken_claims
        self.assertFalse(validate_relationships(bad_data))


# Standalone function wrappers for pytest compatibility
def test_validate_customers():
    TestValidation().setUp()
    tc = TestValidation()
    tc.setUp()
    tc.test_validate_customers()

def test_validate_policies():
    tc = TestValidation()
    tc.setUp()
    tc.test_validate_policies()

def test_validate_claims():
    tc = TestValidation()
    tc.setUp()
    tc.test_validate_claims()

def test_validate_relationships():
    tc = TestValidation()
    tc.setUp()
    tc.test_validate_relationships()


if __name__ == "__main__":
    unittest.main()
