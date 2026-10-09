"""
Unit tests for insurance analysis module (tests/test_analysis.py).

Verifies calculation of insurance KPIs, ratios, and summary metrics using controlled fixtures.
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.insurance_analysis import (
    calculate_total_policies,
    calculate_active_policies,
    calculate_total_claims,
    calculate_total_premium,
    calculate_claim_approval_rate,
    calculate_average_claim_amount,
    calculate_claim_to_premium_ratio
)


class TestAnalysis(unittest.TestCase):
    """Test suite for insurance analytics functions."""

    def setUp(self):
        """Creates small controlled fixtures for testing calculations."""
        self.policies_df = pd.DataFrame({
            "policy_id": ["P1", "P2", "P3", "P4"],
            "policy_status": ["Active", "Active", "Expired", "Renewed"],
            "premium_amount": [10000.0, 20000.0, 15000.0, 25000.0],
            "coverage_amount": [200000.0, 400000.0, 300000.0, 500000.0]
        })

        self.claims_df = pd.DataFrame({
            "claim_id": ["C1", "C2", "C3", "C4"],
            "claim_status": ["Approved", "Settled", "Rejected", "Pending"],
            "claim_amount": [50000.0, 70000.0, 30000.0, 40000.0]
        })

    def test_calculate_total_policies(self):
        """Proves calculate_total_policies returns exact unique count of policies."""
        self.assertEqual(calculate_total_policies(self.policies_df), 4)

    def test_calculate_active_policies(self):
        """Proves calculate_active_policies counts only policies with Active status."""
        self.assertEqual(calculate_active_policies(self.policies_df), 2)

    def test_calculate_total_claims(self):
        """Proves calculate_total_claims returns total registered claims."""
        self.assertEqual(calculate_total_claims(self.claims_df), 4)

    def test_calculate_total_premium(self):
        """Proves calculate_total_premium accurately sums premium amounts."""
        self.assertEqual(calculate_total_premium(self.policies_df), 70000.0)

    def test_calculate_claim_approval_rate(self):
        """Proves calculate_claim_approval_rate calculates approved+settled claims percentage."""
        # 2 approved/settled out of 4 = 50.0%
        rate = calculate_claim_approval_rate(self.claims_df, include_settled=True)
        self.assertEqual(rate, 50.0)

    def test_calculate_average_claim_amount(self):
        """Proves calculate_average_claim_amount computes arithmetic mean of claim amounts."""
        # (50k + 70k + 30k + 40k) / 4 = 47500.0
        avg_amt = calculate_average_claim_amount(self.claims_df)
        self.assertEqual(avg_amt, 47500.0)

    def test_calculate_claim_to_premium_ratio(self):
        """Proves calculate_claim_to_premium_ratio computes total claims over total premium."""
        # Total claims: 190,000 / Total premium: 70,000 = 2.7143
        ratio = calculate_claim_to_premium_ratio(claims_df=self.claims_df, policies_df=self.policies_df)
        self.assertEqual(ratio, 2.7143)


# Standalone function wrappers for pytest compatibility
def test_calculate_total_policies():
    tc = TestAnalysis()
    tc.setUp()
    tc.test_calculate_total_policies()

def test_calculate_active_policies():
    tc = TestAnalysis()
    tc.setUp()
    tc.test_calculate_active_policies()

def test_calculate_total_claims():
    tc = TestAnalysis()
    tc.setUp()
    tc.test_calculate_total_claims()

def test_calculate_total_premium():
    tc = TestAnalysis()
    tc.setUp()
    tc.test_calculate_total_premium()

def test_calculate_claim_approval_rate():
    tc = TestAnalysis()
    tc.setUp()
    tc.test_calculate_claim_approval_rate()

def test_calculate_average_claim_amount():
    tc = TestAnalysis()
    tc.setUp()
    tc.test_calculate_average_claim_amount()


if __name__ == "__main__":
    unittest.main()
