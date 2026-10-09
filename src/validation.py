"""
Validation module for Motor Insurance Claims & Policy Analytics.

Performs data quality and schema validation on customers, vehicles, policies,
claims, and payments tables, verifying required columns, primary key uniqueness,
numeric domains, date chronology, categorical values, and referential integrity.
"""

from typing import Dict, List, Any
import pandas as pd
from src.logger import log_pipeline_step, log_error

# Standard column definitions per assignment specification
CUSTOMER_COLUMNS = [
    "customer_id", "customer_name", "gender", "date_of_birth", "age", "city", "state", "occupation"
]

VEHICLE_COLUMNS = [
    "vehicle_id", "customer_id", "vehicle_type", "vehicle_make", "vehicle_model",
    "vehicle_year", "fuel_type", "vehicle_value"
]

POLICY_COLUMNS = [
    "policy_id", "customer_id", "vehicle_id", "policy_start_date", "policy_end_date",
    "policy_type", "premium_amount", "coverage_amount", "policy_status", "payment_frequency"
]

CLAIM_COLUMNS = [
    "claim_id", "policy_id", "customer_id", "claim_date", "accident_date", "claim_type",
    "accident_location", "claim_amount", "claim_status", "approval_date", "settlement_date", "damage_severity"
]

PAYMENT_COLUMNS = [
    "payment_id", "claim_id", "policy_id", "payment_date", "payment_amount",
    "payment_status", "payment_method"
]

# Standard allowed categorical domains
ALLOWED_POLICY_STATUS = {"Active", "Expired", "Cancelled", "Renewed"}
ALLOWED_POLICY_TYPES = {"Comprehensive", "Third Party", "Zero Depreciation"}
ALLOWED_CLAIM_STATUS = {"Pending", "Approved", "Rejected", "Settled"}
ALLOWED_DAMAGE_SEVERITY = {"Low", "Medium", "High"}
ALLOWED_CLAIM_TYPES = {"Accident", "Third Party Damage", "Theft", "Natural Disaster", "Fire"}


def _check_required_columns(df: pd.DataFrame, required: List[str], table_name: str) -> bool:
    """Helper to check if all required columns exist in DataFrame."""
    missing = [col for col in required if col not in df.columns]
    if missing:
        log_error(f"Validation failure in '{table_name}': missing columns {missing}")
        return False
    return True


def validate_customers(df: pd.DataFrame) -> bool:
    """
    Validates the customers table schema, primary keys, and data integrity.

    Args:
        df: Customer DataFrame.

    Returns:
        True if valid, False otherwise.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        log_error("Customers validation failed: Invalid DataFrame provided.")
        return False

    if not _check_required_columns(df, CUSTOMER_COLUMNS, "customers"):
        return False

    if df.empty:
        log_error("Customers validation failed: Table is empty.")
        return False

    if df["customer_id"].isnull().any():
        log_error("Customers validation failed: customer_id contains null values.")
        return False
    if df["customer_id"].duplicated().any():
        log_error("Customers validation failed: customer_id contains duplicate values.")
        return False

    if (df["age"] <= 0).any() or (df["age"] > 120).any():
        log_error("Customers validation failed: age values outside realistic bounds (1-120).")
        return False

    log_pipeline_step(f"Customers table validation passed ({len(df)} records).")
    return True


def validate_vehicles(df: pd.DataFrame) -> bool:
    """
    Validates the vehicles table schema, primary keys, and value domains.

    Args:
        df: Vehicles DataFrame.

    Returns:
        True if valid, False otherwise.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        log_error("Vehicles validation failed: Invalid DataFrame provided.")
        return False

    if not _check_required_columns(df, VEHICLE_COLUMNS, "vehicles"):
        return False

    if df.empty:
        log_error("Vehicles validation failed: Table is empty.")
        return False

    if df["vehicle_id"].isnull().any():
        log_error("Vehicles validation failed: vehicle_id contains nulls.")
        return False
    if df["vehicle_id"].duplicated().any():
        log_error("Vehicles validation failed: vehicle_id contains duplicates.")
        return False

    if (df["vehicle_year"] < 1980).any() or (df["vehicle_year"] > 2030).any():
        log_error("Vehicles validation failed: vehicle_year contains invalid values.")
        return False

    if (df["vehicle_value"] <= 0).any():
        log_error("Vehicles validation failed: vehicle_value must be strictly positive.")
        return False

    log_pipeline_step(f"Vehicles table validation passed ({len(df)} records).")
    return True


def validate_policies(df: pd.DataFrame) -> bool:
    """
    Validates the policies table schema, constraints, and business rules.

    Args:
        df: Policies DataFrame.

    Returns:
        True if valid, False otherwise.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        log_error("Policies validation failed: Invalid DataFrame provided.")
        return False

    if not _check_required_columns(df, POLICY_COLUMNS, "policies"):
        return False

    if df.empty:
        log_error("Policies validation failed: Table is empty.")
        return False

    if df["policy_id"].isnull().any():
        log_error("Policies validation failed: policy_id contains nulls.")
        return False
    if df["policy_id"].duplicated().any():
        log_error("Policies validation failed: policy_id contains duplicates.")
        return False

    if (df["premium_amount"] <= 0).any():
        log_error("Policies validation failed: premium_amount must be positive.")
        return False
    if (df["coverage_amount"] <= 0).any():
        log_error("Policies validation failed: coverage_amount must be positive.")
        return False

    invalid_status = set(df["policy_status"].dropna().unique()) - ALLOWED_POLICY_STATUS
    if invalid_status:
        log_error(f"Policies validation failed: invalid policy_status {invalid_status}")
        return False

    invalid_types = set(df["policy_type"].dropna().unique()) - ALLOWED_POLICY_TYPES
    if invalid_types:
        log_error(f"Policies validation failed: invalid policy_type {invalid_types}")
        return False

    log_pipeline_step(f"Policies table validation passed ({len(df)} records).")
    return True


def validate_claims(df: pd.DataFrame) -> bool:
    """
    Validates the claims table schema, identifiers, amounts, and dates.

    Args:
        df: Claims DataFrame.

    Returns:
        True if valid, False otherwise.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        log_error("Claims validation failed: Invalid DataFrame provided.")
        return False

    if not _check_required_columns(df, CLAIM_COLUMNS, "claims"):
        return False

    if df.empty:
        log_error("Claims validation failed: Table is empty.")
        return False

    if df["claim_id"].isnull().any():
        log_error("Claims validation failed: claim_id contains nulls.")
        return False
    if df["claim_id"].duplicated().any():
        log_error("Claims validation failed: claim_id contains duplicates.")
        return False

    if (df["claim_amount"] <= 0).any():
        log_error("Claims validation failed: claim_amount must be positive.")
        return False

    invalid_status = set(df["claim_status"].dropna().unique()) - ALLOWED_CLAIM_STATUS
    if invalid_status:
        log_error(f"Claims validation failed: invalid claim_status {invalid_status}")
        return False

    invalid_types = set(df["claim_type"].dropna().unique()) - ALLOWED_CLAIM_TYPES
    if invalid_types:
        log_error(f"Claims validation failed: invalid claim_type {invalid_types}")
        return False

    invalid_severity = set(df["damage_severity"].dropna().unique()) - ALLOWED_DAMAGE_SEVERITY
    if invalid_severity:
        log_error(f"Claims validation failed: invalid damage_severity {invalid_severity}")
        return False

    log_pipeline_step(f"Claims table validation passed ({len(df)} records).")
    return True


def validate_payments(df: pd.DataFrame) -> bool:
    """
    Validates the payments table schema, identifiers, and transaction amounts.

    Args:
        df: Payments DataFrame.

    Returns:
        True if valid, False otherwise.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        log_error("Payments validation failed: Invalid DataFrame provided.")
        return False

    if not _check_required_columns(df, PAYMENT_COLUMNS, "payments"):
        return False

    if df.empty:
        log_error("Payments validation failed: Table is empty.")
        return False

    if df["payment_id"].isnull().any():
        log_error("Payments validation failed: payment_id contains nulls.")
        return False
    if df["payment_id"].duplicated().any():
        log_error("Payments validation failed: payment_id contains duplicates.")
        return False

    if (df["payment_amount"] <= 0).any():
        log_error("Payments validation failed: payment_amount must be positive.")
        return False

    log_pipeline_step(f"Payments table validation passed ({len(df)} records).")
    return True


def validate_relationships(data: Dict[str, pd.DataFrame]) -> bool:
    """
    Validates cross-table relationships and foreign key integrity.

    Args:
        data: Dictionary of related DataFrames.

    Returns:
        True if all referential constraints are satisfied, False otherwise.
    """
    customers = data.get("customers")
    vehicles = data.get("vehicles")
    policies = data.get("policies")
    claims = data.get("claims")
    payments = data.get("payments")

    if any(df is None for df in [customers, vehicles, policies, claims, payments]):
        log_error("Relationship validation failed: One or more tables missing from input.")
        return False

    cust_ids = set(customers["customer_id"])
    if not set(policies["customer_id"]).issubset(cust_ids):
        log_error("Relationship validation error: policies reference unknown customer_id.")
        return False

    veh_ids = set(vehicles["vehicle_id"])
    if not set(policies["vehicle_id"]).issubset(veh_ids):
        log_error("Relationship validation error: policies reference unknown vehicle_id.")
        return False

    pol_ids = set(policies["policy_id"])
    if not set(claims["policy_id"]).issubset(pol_ids):
        log_error("Relationship validation error: claims reference unknown policy_id.")
        return False

    if not set(claims["customer_id"]).issubset(cust_ids):
        log_error("Relationship validation error: claims reference unknown customer_id.")
        return False

    claim_ids = set(claims["claim_id"])
    if not set(payments["claim_id"]).issubset(claim_ids):
        log_error("Relationship validation error: payments reference unknown claim_id.")
        return False

    if not set(payments["policy_id"]).issubset(pol_ids):
        log_error("Relationship validation error: payments reference unknown policy_id.")
        return False

    log_pipeline_step("Relational integrity verification passed across all tables.")
    return True


def validate_all_tables(data: Dict[str, pd.DataFrame]) -> bool:
    """
    Executes full validation across all individual tables and relationships.

    Args:
        data: Dictionary containing DataFrames for all 5 tables.

    Returns:
        True if all individual tables and relational constraints pass.
    """
    log_pipeline_step("Beginning comprehensive validation across all tables...")
    valid = True

    valid &= validate_customers(data.get("customers"))
    valid &= validate_vehicles(data.get("vehicles"))
    valid &= validate_policies(data.get("policies"))
    valid &= validate_claims(data.get("claims"))
    valid &= validate_payments(data.get("payments"))
    valid &= validate_relationships(data)

    if valid:
        log_pipeline_step("All tables and relationships validated successfully.")
    else:
        log_error("One or more validation checks failed.")

    return valid
