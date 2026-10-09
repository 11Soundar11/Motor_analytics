"""
Data cleaner module for Motor Insurance Claims & Policy Analytics.

Implements a modular, reusable cleaning pipeline:
- Missing value imputation / formatting
- Duplicate removal
- Text standardization
- Date parsing and normalization
- Numeric validation
- Business rule enforcement
- Feature engineering of derived insurance metrics
- Cleaned table export
"""

import os
from typing import Dict
import numpy as np
import pandas as pd
from src.logger import log_pipeline_step, log_error

ANALYSIS_DATE = pd.to_datetime("2026-10-08")
ANALYSIS_YEAR = 2026


def handle_missing_values(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Handles missing values across all tables according to insurance business logic."""
    log_pipeline_step("Executing handle_missing_values()...")
    cleaned = {k: v.copy() for k, v in data.items()}

    for name, df in cleaned.items():
        text_cols = df.select_dtypes(include=["object"]).columns
        for col in text_cols:
            if col not in ["approval_date", "settlement_date"]:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    df[col] = df[col].fillna("Unknown")
                    log_pipeline_step(f"Imputed {null_count} missing values in {name}.{col} with 'Unknown'.")

        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                log_pipeline_step(f"Imputed {null_count} missing values in {name}.{col} with median ({median_val}).")

    return cleaned


def remove_duplicates(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Removes duplicate records and duplicate primary keys from all tables."""
    log_pipeline_step("Executing remove_duplicates()...")
    cleaned = {}
    pk_map = {
        "customers": "customer_id",
        "vehicles": "vehicle_id",
        "policies": "policy_id",
        "claims": "claim_id",
        "payments": "payment_id"
    }

    for name, df in data.items():
        df_copy = df.copy()
        initial_len = len(df_copy)
        df_copy = df_copy.drop_duplicates()
        pk = pk_map.get(name)
        if pk and pk in df_copy.columns:
            df_copy = df_copy.drop_duplicates(subset=[pk], keep="first")
            
        dropped = initial_len - len(df_copy)
        if dropped > 0:
            log_pipeline_step(f"Removed {dropped} duplicate records from '{name}'.")
        cleaned[name] = df_copy

    return cleaned


def clean_text_columns(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Trims leading/trailing whitespaces and standardizes casing for string fields."""
    log_pipeline_step("Executing clean_text_columns()...")
    cleaned = {}

    for name, df in data.items():
        df_copy = df.copy()
        str_cols = df_copy.select_dtypes(include=["object"]).columns
        for col in str_cols:
            df_copy[col] = df_copy[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
        cleaned[name] = df_copy

    return cleaned


def clean_date_columns(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Parses and standardizes all date fields into datetime64 objects."""
    log_pipeline_step("Executing clean_date_columns()...")
    cleaned = {}

    date_columns_map = {
        "customers": ["date_of_birth"],
        "policies": ["policy_start_date", "policy_end_date"],
        "claims": ["claim_date", "accident_date", "approval_date", "settlement_date"],
        "payments": ["payment_date"]
    }

    for name, df in data.items():
        df_copy = df.copy()
        target_cols = date_columns_map.get(name, [])
        for col in target_cols:
            if col in df_copy.columns:
                df_copy[col] = pd.to_datetime(df_copy[col], errors="coerce")
        cleaned[name] = df_copy

    return cleaned


def validate_numeric_columns(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Validates numeric types, coercing values and verifying positive bounds."""
    log_pipeline_step("Executing validate_numeric_columns()...")
    cleaned = {}

    numeric_columns_map = {
        "customers": ["age"],
        "vehicles": ["vehicle_year", "vehicle_value"],
        "policies": ["premium_amount", "coverage_amount"],
        "claims": ["claim_amount"],
        "payments": ["payment_amount"]
    }

    for name, df in data.items():
        df_copy = df.copy()
        target_cols = numeric_columns_map.get(name, [])
        for col in target_cols:
            if col in df_copy.columns:
                df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
                if col in ["premium_amount", "coverage_amount", "claim_amount", "payment_amount", "vehicle_value"]:
                    df_copy.loc[df_copy[col] < 0, col] = np.nan
        cleaned[name] = df_copy

    return cleaned


def validate_business_rules(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Verifies business logic across dates, status constraints, and claim amounts."""
    log_pipeline_step("Executing validate_business_rules()...")
    cleaned = {k: v.copy() for k, v in data.items()}

    # 1. Policy dates validation
    policies = cleaned.get("policies")
    if policies is not None and "policy_start_date" in policies.columns and "policy_end_date" in policies.columns:
        invalid_policies = policies["policy_end_date"] < policies["policy_start_date"]
        if invalid_policies.any():
            log_pipeline_step(f"Found {invalid_policies.sum()} policies where end_date < start_date (Cancelled status). Adjusting end_date to start_date.")
            policies.loc[invalid_policies, "policy_end_date"] = policies.loc[invalid_policies, "policy_start_date"]
        cleaned["policies"] = policies

    # 2. Claims chronology validation
    claims = cleaned.get("claims")
    if claims is not None:
        invalid_accidents = claims["accident_date"] > claims["claim_date"]
        if invalid_accidents.any():
            log_pipeline_step(f"Found {invalid_accidents.sum()} claims with accident_date > claim_date. Aligning accident_date.")
            claims.loc[invalid_accidents, "accident_date"] = claims.loc[invalid_accidents, "claim_date"]

        has_approval = claims["approval_date"].notnull()
        invalid_approval = has_approval & (claims["approval_date"] < claims["claim_date"])
        if invalid_approval.any():
            log_pipeline_step(f"Found {invalid_approval.sum()} claims with approval_date < claim_date. Aligning approval_date.")
            claims.loc[invalid_approval, "approval_date"] = claims.loc[invalid_approval, "claim_date"]

        has_settlement = claims["settlement_date"].notnull() & claims["approval_date"].notnull()
        invalid_settlement = has_settlement & (claims["settlement_date"] < claims["approval_date"])
        if invalid_settlement.any():
            log_pipeline_step(f"Found {invalid_settlement.sum()} claims with settlement_date < approval_date. Aligning settlement_date.")
            claims.loc[invalid_settlement, "settlement_date"] = claims.loc[invalid_settlement, "approval_date"]

        cleaned["claims"] = claims

    return cleaned


def create_derived_columns(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Creates standardized derived metrics across related tables."""
    log_pipeline_step("Executing create_derived_columns()...")
    augmented = {k: v.copy() for k, v in data.items()}

    customers = augmented.get("customers")
    vehicles = augmented.get("vehicles")
    policies = augmented.get("policies")
    claims = augmented.get("claims")
    payments = augmented.get("payments")

    # 1. Customers derived columns
    if customers is not None and "date_of_birth" in customers.columns:
        dob = pd.to_datetime(customers["date_of_birth"])
        customers["customer_age"] = ANALYSIS_YEAR - dob.dt.year
        augmented["customers"] = customers

    # 2. Vehicles derived columns
    if vehicles is not None and "vehicle_year" in vehicles.columns:
        vehicles["vehicle_age"] = (ANALYSIS_YEAR - vehicles["vehicle_year"]).clip(lower=0)
        augmented["vehicles"] = vehicles

    # 3. Policies derived columns
    if policies is not None:
        start_d = pd.to_datetime(policies["policy_start_date"])
        end_d = pd.to_datetime(policies["policy_end_date"])
        policies["policy_duration_days"] = (end_d - start_d).dt.days
        policies["policy_active_flag"] = (policies["policy_status"] == "Active").astype(int)
        augmented["policies"] = policies

    # 4. Claims derived columns
    if claims is not None:
        c_date = pd.to_datetime(claims["claim_date"])
        a_date = pd.to_datetime(claims["approval_date"])
        s_date = pd.to_datetime(claims["settlement_date"])

        claims["claim_processing_days"] = (a_date - c_date).dt.days
        claims["claim_settlement_days"] = (s_date - c_date).dt.days

        if policies is not None:
            policy_sub = policies[["policy_id", "premium_amount", "coverage_amount"]].drop_duplicates("policy_id")
            merge_cols = [c for c in ["premium_amount", "coverage_amount"] if c not in claims.columns]
            if merge_cols:
                claims = claims.merge(policy_sub[["policy_id"] + merge_cols], on="policy_id", how="left")
            claims["claim_to_premium_ratio"] = claims["claim_amount"] / claims["premium_amount"].replace(0, np.nan)
            claims["claim_to_coverage_ratio"] = claims["claim_amount"] / claims["coverage_amount"].replace(0, np.nan)

        augmented["claims"] = claims

    # 5. Payments & claims paid ratio
    if payments is not None:
        if claims is not None:
            claim_sub = claims[["claim_id", "claim_amount"]].drop_duplicates("claim_id")
            if "claim_amount" not in payments.columns:
                payments = payments.merge(claim_sub, on="claim_id", how="left")
            payments["paid_claim_ratio"] = payments["payment_amount"] / payments["claim_amount"].replace(0, np.nan)
            
            pay_agg = payments.groupby("claim_id")["payment_amount"].sum().reset_index()
            pay_agg.columns = ["claim_id", "total_payment_amount"]
            if "total_payment_amount" in augmented["claims"].columns:
                augmented["claims"] = augmented["claims"].drop(columns=["total_payment_amount"])
            augmented["claims"] = augmented["claims"].merge(pay_agg, on="claim_id", how="left")
            augmented["claims"]["total_payment_amount"] = augmented["claims"]["total_payment_amount"].fillna(0.0)
            augmented["claims"]["paid_claim_ratio"] = (
                augmented["claims"]["total_payment_amount"] / augmented["claims"]["claim_amount"].replace(0, np.nan)
            ).fillna(0.0)

        augmented["payments"] = payments

    log_pipeline_step("Derived columns successfully generated for all tables.")
    return augmented


def clean_data(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Executes the end-to-end data cleaning and transformation pipeline."""
    log_pipeline_step("Starting complete clean_data() workflow...")
    step1 = handle_missing_values(data)
    step2 = remove_duplicates(step1)
    step3 = clean_text_columns(step2)
    step4 = clean_date_columns(step3)
    step5 = validate_numeric_columns(step4)
    step6 = validate_business_rules(step5)
    step7 = create_derived_columns(step6)
    log_pipeline_step("Completed clean_data() pipeline successfully.")
    return step7


def save_cleaned_data(data: Dict[str, pd.DataFrame], output_dir: str) -> None:
    """Saves cleaned DataFrames to the specified output directory as CSV files."""
    os.makedirs(output_dir, exist_ok=True)
    log_pipeline_step(f"Saving cleaned tables to '{output_dir}'...")

    for key in ["customers", "vehicles", "policies", "claims", "payments"]:
        df = data.get(key)
        if df is not None:
            filename = f"{key}_cleaned.csv"
            file_path = os.path.join(output_dir, filename)
            df.to_csv(file_path, index=False)
            log_pipeline_step(f"Saved '{filename}' ({len(df)} records).")

    log_pipeline_step("All cleaned datasets successfully exported.")
