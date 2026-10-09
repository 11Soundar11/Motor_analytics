"""
Visualization module for Motor Insurance Claims & Policy Analytics.

Contains all 18 standardized charting functions required by the project specification.
Each function performs required aggregations, styles the plot professionally,
adds titles and axis labels, and returns the matplotlib Figure object.
"""

from typing import Optional, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Configure standard aesthetic theme
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.titlesize": 14,
    "figure.autolayout": True
})

PRIMARY_COLOR = "#1f77b4"
ACCENT_COLOR = "#ff7f0e"
PALETTE = sns.color_palette("deep")


def _resolve_df(arg: Any, data: Optional[Dict[str, pd.DataFrame]], key: str) -> pd.DataFrame:
    """Helper to extract DataFrame from either primary arg or data dictionary."""
    if isinstance(arg, pd.DataFrame):
        return arg
    if isinstance(arg, dict) and key in arg:
        return arg[key]
    if data is not None and key in data:
        return data[key]
    raise ValueError(f"Could not resolve table '{key}' from provided arguments.")


def plot_policy_status(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots the distribution of policies by status (Active, Expired, Cancelled, Renewed)."""
    df = _resolve_df(policies_df, data, "policies")
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = df["policy_status"].value_counts()
    bars = ax.bar(counts.index, counts.values, color=PALETTE[:len(counts)], edgecolor="black", linewidth=0.8)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:,}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Policy Portfolio Distribution by Status", fontweight="bold", pad=12)
    ax.set_xlabel("Policy Status")
    ax.set_ylabel("Number of Policies")
    ax.set_ylim(0, max(counts.values) * 1.15)
    return fig


def plot_policy_type_distribution(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots the proportion and volume of policies by policy type."""
    df = _resolve_df(policies_df, data, "policies")
    fig, ax = plt.subplots(figsize=(6, 5))
    counts = df["policy_type"].value_counts()
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=140,
           colors=sns.color_palette("pastel"), wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Policy Type Market Share", fontweight="bold", pad=12)
    return fig


def plot_premium_by_policy_type(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots total and average premium revenue across policy types."""
    df = _resolve_df(policies_df, data, "policies")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    grouped = df.groupby("policy_type")["premium_amount"].sum() / 1e6  # in millions
    bars = ax.bar(grouped.index, grouped.values, color=sns.color_palette("Blues_r", len(grouped)), edgecolor="black")
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"₹{height:.1f}M",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Total Premium Collection by Policy Type (₹ Millions)", fontweight="bold", pad=12)
    ax.set_xlabel("Policy Type")
    ax.set_ylabel("Total Premium (₹ Millions)")
    ax.set_ylim(0, max(grouped.values) * 1.15)
    return fig


def plot_monthly_claims(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots monthly trend of registered claim volume."""
    df = _resolve_df(claims_df, data, "claims")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    dates = pd.to_datetime(df["claim_date"])
    monthly = df.groupby(dates.dt.to_period("M")).size()
    ax.plot(monthly.index.astype(str), monthly.values, marker="o", color="#d62728", linewidth=2)
    ax.set_title("Monthly Trend of Registered Claims", fontweight="bold", pad=12)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Claims")
    ax.tick_params(axis="x", rotation=45)
    return fig


def plot_claim_status(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots claim count by status (Pending, Approved, Rejected, Settled)."""
    df = _resolve_df(claims_df, data, "claims")
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = df["claim_status"].value_counts()
    bars = ax.bar(counts.index, counts.values, color=sns.color_palette("Set2", len(counts)), edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,} ({h/len(df)*100:.1f}%)",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Claims Distribution by Operational Status", fontweight="bold", pad=12)
    ax.set_xlabel("Claim Status")
    ax.set_ylabel("Number of Claims")
    ax.set_ylim(0, max(counts.values) * 1.15)
    return fig


def plot_claim_type_distribution(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots the frequency of various claim incident types."""
    df = _resolve_df(claims_df, data, "claims")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    counts = df["claim_type"].value_counts()
    bars = ax.barh(counts.index, counts.values, color=sns.color_palette("viridis", len(counts)), edgecolor="black")
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:,}", xy=(w, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9, fontweight="bold")
    ax.set_title("Distribution of Claims by Incident Type", fontweight="bold", pad=12)
    ax.set_xlabel("Number of Claims")
    ax.set_ylabel("Claim Type")
    ax.set_xlim(0, max(counts.values) * 1.15)
    ax.invert_yaxis()
    return fig


def plot_claim_amount_distribution(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots histogram and KDE distribution of claim amounts."""
    df = _resolve_df(claims_df, data, "claims")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    amounts_k = df["claim_amount"] / 1e3
    sns.histplot(amounts_k, bins=40, kde=True, ax=ax, color="#2ca02c", edgecolor="black")
    mean_val = amounts_k.mean()
    median_val = amounts_k.median()
    ax.axvline(mean_val, color="red", linestyle="--", linewidth=1.5, label=f"Mean: ₹{mean_val:.1f}K")
    ax.axvline(median_val, color="blue", linestyle=":", linewidth=1.5, label=f"Median: ₹{median_val:.1f}K")
    ax.set_title("Claim Amount Distribution (₹ Thousands)", fontweight="bold", pad=12)
    ax.set_xlabel("Claim Amount (₹ Thousands)")
    ax.set_ylabel("Claim Frequency")
    ax.legend()
    return fig


def plot_claim_amount_by_vehicle_type(data: Optional[Dict[str, pd.DataFrame]] = None,
                                      claims_df: Optional[pd.DataFrame] = None,
                                      vehicles_df: Optional[pd.DataFrame] = None,
                                      policies_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """Plots claim severity (total and average claim amount) by vehicle type."""
    if data is not None:
        clm = data["claims"]
        veh = data["vehicles"]
        pol = data["policies"]
    else:
        clm = claims_df
        veh = vehicles_df
        pol = policies_df

    fig, ax = plt.subplots(figsize=(7, 4.5))
    vp = pol.merge(veh[["vehicle_id", "vehicle_type"]], on="vehicle_id", how="left")
    vpc = clm.merge(vp[["policy_id", "vehicle_type"]], on="policy_id", how="left")
    grouped = vpc.groupby("vehicle_type")["claim_amount"].agg(["sum", "mean"]).reset_index()

    bars = ax.bar(grouped["vehicle_type"], grouped["sum"] / 1e6, color=PRIMARY_COLOR, edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"Total: ₹{h:.1f}M", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Total Claim Amount by Vehicle Type (₹ Millions)", fontweight="bold", pad=12)
    ax.set_xlabel("Vehicle Type")
    ax.set_ylabel("Total Claim Amount (₹ Millions)")
    ax.set_ylim(0, max(grouped["sum"] / 1e6) * 1.2)
    return fig


def plot_claims_by_region(data: Optional[Dict[str, pd.DataFrame]] = None,
                          claims_df: Optional[pd.DataFrame] = None,
                          customers_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """Plots top states by total claim frequency."""
    if data is not None:
        clm = data["claims"]
        cust = data["customers"]
    else:
        clm = claims_df
        cust = customers_df

    fig, ax = plt.subplots(figsize=(10, 5))
    merged = clm.merge(cust[["customer_id", "state"]], on="customer_id", how="left")
    top_states = merged["state"].value_counts().head(10)
    bars = ax.bar(top_states.index, top_states.values, color=sns.color_palette("mako", len(top_states)), edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,}", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_title("Top 10 States by Claim Frequency", fontweight="bold", pad=12)
    ax.set_xlabel("State")
    ax.set_ylabel("Number of Claims")
    ax.tick_params(axis="x", rotation=35)
    return fig


def plot_claim_severity_by_region(data: Optional[Dict[str, pd.DataFrame]] = None,
                                  claims_df: Optional[pd.DataFrame] = None,
                                  customers_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """Plots top states by average claim severity."""
    if data is not None:
        clm = data["claims"]
        cust = data["customers"]
    else:
        clm = claims_df
        cust = customers_df

    fig, ax = plt.subplots(figsize=(10, 5))
    merged = clm.merge(cust[["customer_id", "state"]], on="customer_id", how="left")
    top_severity = merged.groupby("state")["claim_amount"].mean().sort_values(ascending=False).head(10) / 1e3
    bars = ax.bar(top_severity.index, top_severity.values, color=sns.color_palette("flare", len(top_severity)), edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"₹{h:.1f}K", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_title("Top 10 States by Average Claim Severity (₹ Thousands)", fontweight="bold", pad=12)
    ax.set_xlabel("State")
    ax.set_ylabel("Average Claim Amount (₹ Thousands)")
    ax.tick_params(axis="x", rotation=35)
    return fig


def plot_average_settlement_time(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots average claim settlement duration across claim types."""
    df = _resolve_df(claims_df, data, "claims")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    settled = df[df["claim_status"] == "Settled"].copy()
    if "claim_settlement_days" not in settled.columns:
        settled["claim_settlement_days"] = (pd.to_datetime(settled["settlement_date"]) - pd.to_datetime(settled["claim_date"])).dt.days
    grouped = settled.groupby("claim_type")["claim_settlement_days"].mean().sort_values()
    bars = ax.barh(grouped.index, grouped.values, color="#9467bd", edgecolor="black")
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.1f} days", xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9, fontweight="bold")
    ax.set_title("Average Settlement Time by Claim Type (Days)", fontweight="bold", pad=12)
    ax.set_xlabel("Average Settlement Days")
    ax.set_ylabel("Claim Type")
    ax.set_xlim(0, max(grouped.values) * 1.25)
    return fig


def plot_claim_to_premium_by_policy_type(data: Optional[Dict[str, pd.DataFrame]] = None,
                                         policies_df: Optional[pd.DataFrame] = None,
                                         claims_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """Plots claim-to-premium loss ratio across policy types."""
    if data is not None:
        pol = data["policies"]
        clm = data["claims"]
    else:
        pol = policies_df
        clm = claims_df

    fig, ax = plt.subplots(figsize=(8, 4.5))
    pol_prem = pol.groupby("policy_type")["premium_amount"].sum()
    clm_merged = clm.merge(pol[["policy_id", "policy_type"]], on="policy_id", how="left")
    clm_loss = clm_merged.groupby("policy_type")["claim_amount"].sum()
    ratio = (clm_loss / pol_prem).sort_values(ascending=False)

    bars = ax.bar(ratio.index, ratio.values, color=sns.color_palette("Oranges_r", len(ratio)), edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.2f}x ({h*100:.1f}%)", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.axhline(1.0, color="red", linestyle="--", linewidth=1.2, label="Breakeven Ratio (1.0x)")
    ax.set_title("Claim-to-Premium Loss Ratio by Policy Type", fontweight="bold", pad=12)
    ax.set_xlabel("Policy Type")
    ax.set_ylabel("Loss Ratio (Claim Cost / Premium)")
    ax.set_ylim(0, max(ratio.values) * 1.2)
    ax.legend()
    return fig


def plot_vehicle_age_vs_claim_amount(data: Optional[Dict[str, pd.DataFrame]] = None,
                                     claims_df: Optional[pd.DataFrame] = None,
                                     vehicles_df: Optional[pd.DataFrame] = None,
                                     policies_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """Plots average claim amount against vehicle age."""
    if data is not None:
        clm = data["claims"]
        veh = data["vehicles"]
        pol = data["policies"]
    else:
        clm = claims_df
        veh = vehicles_df
        pol = policies_df

    fig, ax = plt.subplots(figsize=(8, 4.5))
    vp = pol.merge(veh[["vehicle_id", "vehicle_year"]], on="vehicle_id", how="left")
    vpc = clm.merge(vp[["policy_id", "vehicle_year"]], on="policy_id", how="left")
    vpc["vehicle_age"] = 2026 - vpc["vehicle_year"]
    grouped = vpc.groupby("vehicle_age")["claim_amount"].mean() / 1e3

    ax.plot(grouped.index, grouped.values, marker="s", color="#8c564b", linewidth=2)
    ax.set_title("Vehicle Age vs. Average Claim Amount (₹ Thousands)", fontweight="bold", pad=12)
    ax.set_xlabel("Vehicle Age (Years)")
    ax.set_ylabel("Average Claim Amount (₹ Thousands)")
    return fig


def plot_customer_age_vs_claim_amount(data: Optional[Dict[str, pd.DataFrame]] = None,
                                      claims_df: Optional[pd.DataFrame] = None,
                                      customers_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """Plots average claim amount across customer age brackets."""
    if data is not None:
        clm = data["claims"]
        cust = data["customers"]
    else:
        clm = claims_df
        cust = customers_df

    fig, ax = plt.subplots(figsize=(8, 4.5))
    merged = clm.merge(cust[["customer_id", "age"]], on="customer_id", how="left")
    merged["age_bracket"] = pd.cut(merged["age"], bins=[17, 25, 35, 50, 65, 100],
                                   labels=["18-25", "26-35", "36-50", "51-65", "65+"])
    grouped = merged.groupby("age_bracket", observed=False)["claim_amount"].mean() / 1e3

    bars = ax.bar(grouped.index.astype(str), grouped.values, color="#17becf", edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"₹{h:.1f}K", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Customer Age Group vs. Average Claim Amount (₹ Thousands)", fontweight="bold", pad=12)
    ax.set_xlabel("Customer Age Group")
    ax.set_ylabel("Average Claim Amount (₹ Thousands)")
    ax.set_ylim(0, max(grouped.values) * 1.15)
    return fig


def plot_vehicle_type_claim_performance(data: Optional[Dict[str, pd.DataFrame]] = None,
                                        claims_df: Optional[pd.DataFrame] = None,
                                        vehicles_df: Optional[pd.DataFrame] = None,
                                        policies_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """Plots vehicle make claim performance comparing claim count and claim cost."""
    if data is not None:
        clm = data["claims"]
        veh = data["vehicles"]
        pol = data["policies"]
    else:
        clm = claims_df
        veh = vehicles_df
        pol = policies_df

    fig, ax = plt.subplots(figsize=(8, 4.5))
    vp = pol.merge(veh[["vehicle_id", "vehicle_make"]], on="vehicle_id", how="left")
    vpc = clm.merge(vp[["policy_id", "vehicle_make"]], on="policy_id", how="left")
    grouped = vpc.groupby("vehicle_make")["claim_amount"].sum() / 1e6

    bars = ax.bar(grouped.index, grouped.values, color=sns.color_palette("muted", len(grouped)), edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"₹{h:.1f}M", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Total Claim Amount by Vehicle Make (₹ Millions)", fontweight="bold", pad=12)
    ax.set_xlabel("Vehicle Make")
    ax.set_ylabel("Total Claims (₹ Millions)")
    ax.set_ylim(0, max(grouped.values) * 1.15)
    return fig


def plot_damage_severity_distribution(claims_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots claim counts categorized by damage severity level."""
    df = _resolve_df(claims_df, data, "claims")
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = df["damage_severity"].value_counts()
    colors = {"Low": "#2ca02c", "Medium": "#ff7f0e", "High": "#d62728"}
    bar_colors = [colors.get(k, "#1f77b4") for k in counts.index]
    bars = ax.bar(counts.index, counts.values, color=bar_colors, edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,} ({h/len(df)*100:.1f}%)", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Claims Distribution by Damage Severity", fontweight="bold", pad=12)
    ax.set_xlabel("Damage Severity")
    ax.set_ylabel("Number of Claims")
    ax.set_ylim(0, max(counts.values) * 1.15)
    return fig


def plot_payment_status(payments_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots distribution of payment settlement status and methods."""
    df = _resolve_df(payments_df, data, "payments")
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = df["payment_method"].value_counts()
    bars = ax.bar(counts.index, counts.values, color=sns.color_palette("Set3", len(counts)), edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,}", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Claim Settlement Payment Method Distribution", fontweight="bold", pad=12)
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Transaction Count")
    ax.set_ylim(0, max(counts.values) * 1.15)
    return fig


def plot_monthly_premium_trend(policies_df: Optional[pd.DataFrame] = None, data: Optional[Dict[str, pd.DataFrame]] = None) -> plt.Figure:
    """Plots monthly trend of policy underwriting and premium collections."""
    df = _resolve_df(policies_df, data, "policies")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    dates = pd.to_datetime(df["policy_start_date"])
    monthly = (df.groupby(dates.dt.to_period("M"))["premium_amount"].sum() / 1e6)
    ax.plot(monthly.index.astype(str), monthly.values, marker="o", color="#1f77b4", linewidth=2)
    ax.set_title("Monthly Underwritten Premium Trend (₹ Millions)", fontweight="bold", pad=12)
    ax.set_xlabel("Policy Start Month")
    ax.set_ylabel("Premium Collected (₹ Millions)")
    ax.tick_params(axis="x", rotation=45)
    return fig
