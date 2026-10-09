"""
Streamlit Web Application for Motor Insurance Claims & Policy Analytics.

Features:
- Dynamic sidebar filtering across Policy Type, Policy Status, Claim Status, Claim Type,
  Vehicle Make, Vehicle Type, State/City, and Damage Severity.
- Executive Overview dashboard with high-impact metric cards and loss indicators.
- In-depth analytical views across Policies, Claims, Customers, Vehicles, and Risk Ratios.
- Dynamic Insight & Pattern Engine rendering evidence-grounded recommendation cards.
"""

import sys
import os
import streamlit as st
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import src.insurance_analysis as ia
import src.visualization as viz
import src.insights as ins
from src.data_loader import load_all_data


@st.cache_data
def load_dashboard_data() -> dict:
    """
    Loads cleaned motor insurance datasets with caching for responsive UI.
    """
    data_path = os.path.join(PROJECT_ROOT, "data", "cleaned")
    # Fallback to raw if cleaned not yet generated
    if not os.path.exists(os.path.join(data_path, "policies_cleaned.csv")):
        data_path = os.path.join(PROJECT_ROOT, "data", "raw")
    return load_all_data(data_path)


def show_sidebar_filters(data: dict) -> dict:
    """
    Renders multi-select and range filters in the Streamlit sidebar.
    Returns filtered subsets of all related tables.
    """
    st.sidebar.title("🔍 Portfolio Filters")
    st.sidebar.markdown("Filter active records across operational dimensions:")

    policies = data["policies"].copy()
    claims = data["claims"].copy()
    customers = data["customers"].copy()
    vehicles = data["vehicles"].copy()
    payments = data["payments"].copy()

    # 1. Policy Filters
    pol_types = ["All"] + sorted(policies["policy_type"].dropna().unique().tolist())
    sel_pol_type = st.sidebar.selectbox("Policy Type", pol_types)
    if sel_pol_type != "All":
        policies = policies[policies["policy_type"] == sel_pol_type]

    pol_statuses = ["All"] + sorted(policies["policy_status"].dropna().unique().tolist())
    sel_pol_status = st.sidebar.selectbox("Policy Status", pol_statuses)
    if sel_pol_status != "All":
        policies = policies[policies["policy_status"] == sel_pol_status]

    # 2. Claim Filters
    claim_types = ["All"] + sorted(claims["claim_type"].dropna().unique().tolist())
    sel_claim_type = st.sidebar.selectbox("Claim Type", claim_types)
    if sel_claim_type != "All":
        claims = claims[claims["claim_type"] == sel_claim_type]

    claim_statuses = ["All"] + sorted(claims["claim_status"].dropna().unique().tolist())
    sel_claim_status = st.sidebar.selectbox("Claim Status", claim_statuses)
    if sel_claim_status != "All":
        claims = claims[claims["claim_status"] == sel_claim_status]

    severities = ["All"] + sorted(claims["damage_severity"].dropna().unique().tolist())
    sel_severity = st.sidebar.selectbox("Damage Severity", severities)
    if sel_severity != "All":
        claims = claims[claims["damage_severity"] == sel_severity]

    # 3. Vehicle Filters
    makes = ["All"] + sorted(vehicles["vehicle_make"].dropna().unique().tolist())
    sel_make = st.sidebar.selectbox("Vehicle Make", makes)
    if sel_make != "All":
        vehicles = vehicles[vehicles["vehicle_make"] == sel_make]

    # 4. Geography Filters
    states = ["All"] + sorted(customers["state"].dropna().unique().tolist())
    sel_state = st.sidebar.selectbox("State / Region", states)
    if sel_state != "All":
        customers = customers[customers["state"] == sel_state]

    # Synchronize relational constraints
    valid_cust_ids = set(customers["customer_id"])
    valid_veh_ids = set(vehicles["vehicle_id"])
    policies = policies[policies["customer_id"].isin(valid_cust_ids) & policies["vehicle_id"].isin(valid_veh_ids)]

    valid_pol_ids = set(policies["policy_id"])
    claims = claims[claims["policy_id"].isin(valid_pol_ids)]

    valid_claim_ids = set(claims["claim_id"])
    payments = payments[payments["claim_id"].isin(valid_claim_ids)]

    st.sidebar.markdown("---")
    st.sidebar.info(f"Filtered: {len(policies):,} policies | {len(claims):,} claims")

    return {
        "customers": customers,
        "vehicles": vehicles,
        "policies": policies,
        "claims": claims,
        "payments": payments
    }


def show_overview(data: dict):
    """Renders Executive Overview page with primary KPI metrics and high-level charts."""
    st.title("📊 Executive Overview & Portfolio Health")
    st.markdown("High-level executive dashboard tracking policy volumes, premium collections, and claim liabilities.")

    # KPI Top Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    tot_policies = ia.calculate_total_policies(data=data)
    active_policies = ia.calculate_active_policies(data=data)
    tot_premium = ia.calculate_total_premium(data=data)
    tot_claims = ia.calculate_total_claims(data=data)

    c1.metric("Total Policies", f"{tot_policies:,}")
    c2.metric("Active Policies", f"{active_policies:,}", f"{(active_policies/tot_policies*100 if tot_policies else 0):.1f}%")
    c3.metric("Total Premium", f"₹{tot_premium/1e6:,.1f}M")
    c4.metric("Total Claims", f"{tot_claims:,}")

    c5, c6, c7, c8 = st.columns(4)
    tot_claim_amt = ia.calculate_total_claim_amount(data=data)
    approval_rate = ia.calculate_claim_approval_rate(data=data)
    settle_days = ia.calculate_average_claim_settlement_days(data=data)
    loss_ratio = ia.calculate_claim_to_premium_ratio(data=data)

    c5.metric("Total Claim Amount", f"₹{tot_claim_amt/1e6:,.1f}M")
    c6.metric("Claim Approval Rate", f"{approval_rate:.1f}%")
    c7.metric("Avg Settlement Time", f"{settle_days:.1f} days")
    c8.metric("Loss Ratio (Claim/Prem)", f"{loss_ratio:.2f}x")

    st.markdown("---")

    # Overview Visuals
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Policy Portfolio by Status")
        fig1 = viz.plot_policy_status(data=data)
        st.pyplot(fig1)

    with col_right:
        st.subheader("Claims Operational Status")
        fig2 = viz.plot_claim_status(data=data)
        st.pyplot(fig2)


def show_policy_analysis(data: dict):
    """Renders Policy Analysis page covering status, types, and premium trends."""
    st.title("📋 Policy Portfolio & Underwriting Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Policy Type Market Share")
        fig1 = viz.plot_policy_type_distribution(data=data)
        st.pyplot(fig1)

    with col2:
        st.subheader("Premium Revenue by Policy Type")
        fig2 = viz.plot_premium_by_policy_type(data=data)
        st.pyplot(fig2)

    st.subheader("Monthly Policy Underwriting Trend")
    fig3 = viz.plot_monthly_premium_trend(data=data)
    st.pyplot(fig3)


def show_claim_analysis(data: dict):
    """Renders Claims Analysis page with severity, types, and settlement efficiency."""
    st.title("🚨 Claims Behavior & Settlement Operations")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Claims by Incident Type")
        fig1 = viz.plot_claim_type_distribution(data=data)
        st.pyplot(fig1)

    with col2:
        st.subheader("Damage Severity Distribution")
        fig2 = viz.plot_damage_severity_distribution(data=data)
        st.pyplot(fig2)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Claim Amount Distribution")
        fig3 = viz.plot_claim_amount_distribution(data=data)
        st.pyplot(fig3)

    with col4:
        st.subheader("Average Settlement Duration (Days)")
        fig4 = viz.plot_average_settlement_time(data=data)
        st.pyplot(fig4)

    st.subheader("Monthly Claim Frequency")
    fig5 = viz.plot_monthly_claims(data=data)
    st.pyplot(fig5)


def show_customer_analysis(data: dict):
    """Renders Customer Analysis page covering demographics, occupations, and age brackets."""
    st.title("👥 Customer Profile & Demographic Segmentation")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Customer Age vs. Claim Severity")
        fig1 = viz.plot_customer_age_vs_claim_amount(data=data)
        st.pyplot(fig1)

    with col2:
        st.subheader("Top Geographic Markets by Claim Volume")
        fig2 = viz.plot_claims_by_region(data=data)
        st.pyplot(fig2)

    st.subheader("Claims Frequency by Customer Occupation")
    cust_claims = ia.analyze_customer_claims(data)
    st.dataframe(cust_claims.head(10), use_container_width=True)


def show_vehicle_analysis(data: dict):
    """Renders Vehicle Analysis page covering vehicle makes, types, fuel, and age."""
    st.title("🚗 Vehicle Profile & Risk Exposure")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Claim Severity by Vehicle Make")
        fig1 = viz.plot_vehicle_type_claim_performance(data=data)
        st.pyplot(fig1)

    with col2:
        st.subheader("Vehicle Age vs. Claim Amount")
        fig2 = viz.plot_vehicle_age_vs_claim_amount(data=data)
        st.pyplot(fig2)

    st.subheader("Vehicle Claims Performance by Manufacturer & Fuel Type")
    veh_summary = ia.analyze_vehicle_claims(data)
    st.dataframe(veh_summary.head(10), use_container_width=True)


def show_premium_analysis(data: dict):
    """Renders Premium & Risk page analyzing loss ratios and regional risk."""
    st.title("⚖️ Premium Collections & Underwriting Risk")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Loss Ratio by Policy Type (Claim / Premium)")
        fig1 = viz.plot_claim_to_premium_by_policy_type(data=data)
        st.pyplot(fig1)

    with col2:
        st.subheader("Claim Severity by State")
        fig2 = viz.plot_claim_severity_by_region(data=data)
        st.pyplot(fig2)

    st.subheader("Payment Settlement Methods")
    fig3 = viz.plot_payment_status(data=data)
    st.pyplot(fig3)


def show_insights(data: dict):
    """
    Renders dynamically generated Pattern, Evidence, Business Meaning, and Recommendations.
    """
    st.title("💡 Dynamic Insights & Actionable Recommendations")
    st.markdown("Automated pattern detection grounded directly in the currently active dataset/filtered portfolio.")

    tab1, tab2, tab3, tab4 = st.tabs(["Portfolio & Premium", "Claims & Operations", "Customer & Vehicle Risk", "Strategic Actions"])

    with tab1:
        st.subheader("Portfolio & Premium Patterns")
        insights_port = ins.generate_portfolio_insights(data) + ins.generate_premium_insights(data)
        for item in insights_port:
            with st.expander(f"📌 {item['pattern']}", expanded=True):
                st.markdown(f"**Evidence:** {item['evidence']}")
                st.markdown(f"**Business Meaning:** {item['business_meaning']}")
                st.info(f"**Recommended Action:** {item['recommendation']}")

    with tab2:
        st.subheader("Claims Operational Patterns")
        insights_claim = ins.generate_claim_insights(data)
        for item in insights_claim:
            with st.expander(f"📌 {item['pattern']}", expanded=True):
                st.markdown(f"**Evidence:** {item['evidence']}")
                st.markdown(f"**Business Meaning:** {item['business_meaning']}")
                st.info(f"**Recommended Action:** {item['recommendation']}")

    with tab3:
        st.subheader("Demographic & Vehicle Asset Risk")
        insights_veh = ins.generate_customer_insights(data) + ins.generate_vehicle_insights(data) + ins.generate_risk_patterns(data)
        for item in insights_veh:
            with st.expander(f"📌 {item['pattern']}", expanded=True):
                st.markdown(f"**Evidence:** {item['evidence']}")
                st.markdown(f"**Business Meaning:** {item['business_meaning']}")
                st.info(f"**Recommended Action:** {item['recommendation']}")

    with tab4:
        st.subheader("Executive Strategic Recommendations")
        recs = ins.generate_business_recommendations(data)
        for item in recs:
            with st.expander(f"🎯 {item['pattern']}", expanded=True):
                st.markdown(f"**Current Evidence:** {item['evidence']}")
                st.markdown(f"**Underwriting Implication:** {item['business_meaning']}")
                st.success(f"**Action Plan:** {item['recommendation']}")


def main():
    """Application main entry point."""
    st.set_page_config(
        page_title="Motor Insurance Analytics",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    raw_data = load_dashboard_data()
    filtered_data = show_sidebar_filters(raw_data)

    pages = {
        "Executive Overview": show_overview,
        "Policy Analysis": show_policy_analysis,
        "Claims Analysis": show_claim_analysis,
        "Customer Analysis": show_customer_analysis,
        "Vehicle Analysis": show_vehicle_analysis,
        "Premium & Risk": show_premium_analysis,
        "Insights & Recommendations": show_insights
    }

    st.sidebar.markdown("---")
    selected_page = st.sidebar.radio("Navigation", list(pages.keys()))

    # Render selected page
    pages[selected_page](filtered_data)


if __name__ == "__main__":
    main()
