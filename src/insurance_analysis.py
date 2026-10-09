"""
Insurance Analysis module for Motor Insurance Claims & Policy Analytics.

Implements all standardized business metrics, insurance KPIs, customer/vehicle
segmentation analyses, and loss ratio calculations.
"""

from typing import Dict, Any, Union, Optional
import numpy as np
import pandas as pd


def _get_df(obj: Any, key: str) -> pd.DataFrame:
    """Helper to extract a DataFrame from either a dictionary or direct DataFrame."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        raise KeyError(f"Table '{key}' not found in provided data dictionary.")
    if isinstance(obj, pd.DataFrame):
        return obj
    raise TypeError(f"Expected pandas DataFrame or dictionary, got {type(obj)}")


# ============================================================================
# 1. PORTFOLIO KPIS
# ============================================================================

def calculate_total_customers(customers_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the total count of unique customers."""
    df = customers_df if customers_df is not None else _get_df(data, "customers")
    return int(df["customer_id"].nunique()) if "customer_id" in df.columns else len(df)


def calculate_total_policies(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the total count of policies in the portfolio."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    return int(df["policy_id"].nunique()) if "policy_id" in df.columns else len(df)


def calculate_active_policies(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the count of currently Active policies."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    if "policy_status" in df.columns:
        return int((df["policy_status"] == "Active").sum())
    return 0


def calculate_expired_policies(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the count of Expired policies."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    if "policy_status" in df.columns:
        return int((df["policy_status"] == "Expired").sum())
    return 0


def calculate_cancelled_policies(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the count of Cancelled policies."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    if "policy_status" in df.columns:
        return int((df["policy_status"] == "Cancelled").sum())
    return 0


def calculate_renewed_policies(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the count of Renewed policies."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    if "policy_status" in df.columns:
        return int((df["policy_status"] == "Renewed").sum())
    return 0


# ============================================================================
# 2. PREMIUM & COVERAGE KPIS
# ============================================================================

def calculate_total_premium(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates the total sum of premium collected across all policies."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    return float(df["premium_amount"].sum()) if "premium_amount" in df.columns else 0.0


def calculate_average_premium(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates the average premium amount per policy."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    return float(df["premium_amount"].mean()) if "premium_amount" in df.columns and len(df) > 0 else 0.0


def calculate_average_coverage(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates the average insured coverage amount per policy."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    return float(df["coverage_amount"].mean()) if "coverage_amount" in df.columns and len(df) > 0 else 0.0


def calculate_premium_by_policy_type(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> pd.Series:
    """Calculates the total premium grouped by policy type."""
    df = policies_df if policies_df is not None else _get_df(data, "policies")
    if "policy_type" in df.columns and "premium_amount" in df.columns:
        return df.groupby("policy_type")["premium_amount"].sum()
    return pd.Series(dtype=float)


# ============================================================================
# 3. CLAIMS KPIS
# ============================================================================

def calculate_total_claims(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the total number of registered claims."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    return int(df["claim_id"].nunique()) if "claim_id" in df.columns else len(df)


def calculate_approved_claims(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None, include_settled: bool = True) -> int:
    """
    Calculates the count of claims that were approved.
    If include_settled is True, includes claims that progressed from Approved to Settled.
    """
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    if "claim_status" not in df.columns:
        return 0
    if include_settled:
        return int(df["claim_status"].isin(["Approved", "Settled"]).sum())
    return int((df["claim_status"] == "Approved").sum())


def calculate_rejected_claims(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the count of Rejected claims."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    if "claim_status" in df.columns:
        return int((df["claim_status"] == "Rejected").sum())
    return 0


def calculate_pending_claims(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> int:
    """Calculates the count of Pending claims."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    if "claim_status" in df.columns:
        return int((df["claim_status"] == "Pending").sum())
    return 0


def calculate_total_claim_amount(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates the total claim amount requested across all claims."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    return float(df["claim_amount"].sum()) if "claim_amount" in df.columns else 0.0


def calculate_average_claim_amount(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates the average claim amount requested per claim."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    return float(df["claim_amount"].mean()) if "claim_amount" in df.columns and len(df) > 0 else 0.0


def calculate_claim_approval_rate(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None, include_settled: bool = True) -> float:
    """Calculates claim approval rate as percentage of total claims."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    if len(df) == 0:
        return 0.0
    approved = calculate_approved_claims(df, include_settled=include_settled)
    return round((approved / len(df)) * 100.0, 2)


def calculate_claim_rejection_rate(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates claim rejection rate as percentage of total claims."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    if len(df) == 0:
        return 0.0
    rejected = calculate_rejected_claims(df)
    return round((rejected / len(df)) * 100.0, 2)


# ============================================================================
# 4. SETTLEMENT & PAYMENT KPIS
# ============================================================================

def calculate_average_claim_processing_days(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates average processing duration in days (approval_date - claim_date)."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    if "claim_processing_days" in df.columns:
        valid_days = df["claim_processing_days"].dropna()
        return float(valid_days.mean()) if len(valid_days) > 0 else 0.0
    if "approval_date" in df.columns and "claim_date" in df.columns:
        diff = (pd.to_datetime(df["approval_date"]) - pd.to_datetime(df["claim_date"])).dt.days.dropna()
        return float(diff.mean()) if len(diff) > 0 else 0.0
    return 0.0


def calculate_average_claim_settlement_days(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates average settlement duration in days (settlement_date - claim_date)."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    if "claim_settlement_days" in df.columns:
        valid_days = df["claim_settlement_days"].dropna()
        return float(valid_days.mean()) if len(valid_days) > 0 else 0.0
    if "settlement_date" in df.columns and "claim_date" in df.columns:
        diff = (pd.to_datetime(df["settlement_date"]) - pd.to_datetime(df["claim_date"])).dt.days.dropna()
        return float(diff.mean()) if len(diff) > 0 else 0.0
    return 0.0


def calculate_total_payment_amount(payments_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates total payment disbursed across all claim settlements."""
    df = payments_df if payments_df is not None else _get_df(data, "payments")
    return float(df["payment_amount"].sum()) if "payment_amount" in df.columns else 0.0


def calculate_average_payment_amount(payments_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> float:
    """Calculates average payment amount per settlement transaction."""
    df = payments_df if payments_df is not None else _get_df(data, "payments")
    return float(df["payment_amount"].mean()) if "payment_amount" in df.columns and len(df) > 0 else 0.0


# ============================================================================
# 5. RISK & RATIO KPIS
# ============================================================================

def calculate_claim_to_premium_ratio(data: Optional[Dict[str, pd.DataFrame]] = None,
                                     claims_df: Optional[pd.DataFrame] = None,
                                     policies_df: Optional[pd.DataFrame] = None) -> float:
    """Calculates portfolio Claim-to-Premium loss ratio."""
    if claims_df is None and data is not None:
        claims_df = data.get("claims")
    if policies_df is None and data is not None:
        policies_df = data.get("policies")

    tot_claims = float(claims_df["claim_amount"].sum()) if claims_df is not None and "claim_amount" in claims_df.columns else 0.0
    tot_prem = float(policies_df["premium_amount"].sum()) if policies_df is not None and "premium_amount" in policies_df.columns else 0.0

    return round(tot_claims / tot_prem, 4) if tot_prem > 0 else 0.0


def calculate_claim_to_coverage_ratio(data: Optional[Dict[str, pd.DataFrame]] = None,
                                      claims_df: Optional[pd.DataFrame] = None,
                                      policies_df: Optional[pd.DataFrame] = None) -> float:
    """Calculates portfolio Claim-to-Coverage ratio."""
    if claims_df is None and data is not None:
        claims_df = data.get("claims")
    if policies_df is None and data is not None:
        policies_df = data.get("policies")

    tot_claims = float(claims_df["claim_amount"].sum()) if claims_df is not None and "claim_amount" in claims_df.columns else 0.0
    tot_cov = float(policies_df["coverage_amount"].sum()) if policies_df is not None and "coverage_amount" in policies_df.columns else 0.0

    return round(tot_claims / tot_cov, 4) if tot_cov > 0 else 0.0


def calculate_paid_claim_ratio(data: Optional[Dict[str, pd.DataFrame]] = None,
                               payments_df: Optional[pd.DataFrame] = None,
                               claims_df: Optional[pd.DataFrame] = None) -> float:
    """Calculates Paid Claim Ratio."""
    if payments_df is None and data is not None:
        payments_df = data.get("payments")
    if claims_df is None and data is not None:
        claims_df = data.get("claims")

    tot_pay = float(payments_df["payment_amount"].sum()) if payments_df is not None and "payment_amount" in payments_df.columns else 0.0
    tot_claim = float(claims_df["claim_amount"].sum()) if claims_df is not None and "claim_amount" in claims_df.columns else 0.0

    return round(tot_pay / tot_claim, 4) if tot_claim > 0 else 0.0


# ============================================================================
# 6. CUSTOMER & VEHICLE SEGMENTATION ANALYSES
# ============================================================================

def analyze_customer_claims(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Analyzes claim frequency, severity, and total loss across customer segments."""
    customers = data["customers"]
    claims = data["claims"]
    merged = claims.merge(customers, on="customer_id", how="left")

    if "age" in merged.columns:
        bins = [17, 25, 35, 50, 65, 100]
        labels = ["18-25", "26-35", "36-50", "51-65", "65+"]
        merged["age_group"] = pd.cut(merged["age"], bins=bins, labels=labels)

    summary = merged.groupby("occupation").agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index().sort_values("total_claim_amount", ascending=False)

    return summary


def analyze_customer_premium(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Analyzes policy distribution and premium contribution across customer segments."""
    customers = data["customers"]
    policies = data["policies"]
    merged = policies.merge(customers, on="customer_id", how="left")

    summary = merged.groupby("occupation").agg(
        policy_count=("policy_id", "count"),
        total_premium=("premium_amount", "sum"),
        average_premium=("premium_amount", "mean"),
    ).reset_index().sort_values("total_premium", ascending=False)

    return summary


def analyze_vehicle_claims(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Analyzes claim behavior across vehicle makes and fuel types."""
    vehicles = data["vehicles"]
    policies = data["policies"]
    claims = data["claims"]

    vp = policies.merge(vehicles, on="vehicle_id", how="left", suffixes=("_pol", "_veh"))
    vpc = claims.merge(vp, on="policy_id", how="left", suffixes=("_claim", "_policy"))

    summary = vpc.groupby(["vehicle_make", "fuel_type"]).agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index().sort_values("total_claim_amount", ascending=False)

    return summary


def analyze_vehicle_risk_patterns(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Assesses vehicle risk patterns across vehicle age brackets."""
    vehicles = data["vehicles"]
    policies = data["policies"]
    claims = data["claims"]

    vp = policies.merge(vehicles, on="vehicle_id", how="left")
    vpc = claims.merge(vp, on="policy_id", how="left")

    if "vehicle_age" in vpc.columns:
        vpc["vehicle_age_group"] = pd.cut(
            vpc["vehicle_age"],
            bins=[-1, 2, 5, 8, 15],
            labels=["New (0-2 yrs)", "Moderate (3-5 yrs)", "Aging (6-8 yrs)", "Old (9+ yrs)"]
        )
    else:
        vpc["vehicle_age_group"] = "Unknown"

    summary = vpc.groupby("vehicle_age_group", observed=False).agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean")
    ).reset_index()

    return summary


# ============================================================================
# 7. BUSINESS DIMENSION ANALYSES
# ============================================================================

def analyze_claim_type(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> pd.DataFrame:
    """Analyzes distribution, severity, and approval dynamics by claim type."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    summary = df.groupby("claim_type").agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index().sort_values("claim_count", ascending=False)
    summary["percentage_of_total_claims"] = round((summary["claim_count"] / len(df)) * 100, 2)
    return summary


def analyze_claim_status(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> pd.DataFrame:
    """Analyzes volume and requested amounts across claim statuses."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    summary = df.groupby("claim_status").agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean")
    ).reset_index().sort_values("claim_count", ascending=False)
    summary["percentage"] = round((summary["claim_count"] / len(df)) * 100, 2)
    return summary


def analyze_policy_type(policies_df: Optional[pd.DataFrame] = None,
                        claims_df: Optional[pd.DataFrame] = None,
                        data: Optional[Dict[str, pd.DataFrame]] = None) -> pd.DataFrame:
    """Analyzes policy distribution, total premium, total claims, and loss ratio by policy type."""
    pol = policies_df if policies_df is not None else _get_df(data, "policies")
    clm = claims_df if claims_df is not None else (data.get("claims") if data else None)

    summary = pol.groupby("policy_type").agg(
        policy_count=("policy_id", "count"),
        total_premium=("premium_amount", "sum"),
        average_premium=("premium_amount", "mean"),
        total_coverage=("coverage_amount", "sum")
    ).reset_index()

    if clm is not None:
        merged_clm = clm.merge(pol[["policy_id", "policy_type"]], on="policy_id", how="left")
        clm_summary = merged_clm.groupby("policy_type").agg(
            claim_count=("claim_id", "count"),
            total_claim_amount=("claim_amount", "sum")
        ).reset_index()
        summary = summary.merge(clm_summary, on="policy_type", how="left").fillna(0)
        summary["claim_to_premium_ratio"] = round(summary["total_claim_amount"] / summary["total_premium"], 4)

    return summary


def analyze_region(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Analyzes claims and premium behavior across geographical states and cities."""
    customers = data["customers"]
    claims = data["claims"]
    merged = claims.merge(customers[["customer_id", "city", "state"]], on="customer_id", how="left")

    summary = merged.groupby(["state"]).agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean")
    ).reset_index().sort_values("claim_count", ascending=False)

    return summary


def analyze_vehicle_type(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Analyzes claims performance across vehicle types."""
    vehicles = data["vehicles"]
    policies = data["policies"]
    claims = data["claims"]

    vp = policies.merge(vehicles[["vehicle_id", "vehicle_type"]], on="vehicle_id", how="left")
    vpc = claims.merge(vp, on="policy_id", how="left")

    summary = vpc.groupby("vehicle_type").agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean")
    ).reset_index().sort_values("total_claim_amount", ascending=False)

    return summary


def analyze_damage_severity(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> pd.DataFrame:
    """Analyzes claims volume, average severity amount, and settlement time by damage severity."""
    df = claims_df if claims_df is not None else _get_df(data, "claims")
    summary = df.groupby("damage_severity").agg(
        claim_count=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
        average_settlement_days=("claim_settlement_days", "mean") if "claim_settlement_days" in df.columns else ("claim_amount", "count")
    ).reset_index()
    return summary
