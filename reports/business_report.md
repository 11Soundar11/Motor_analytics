# Motor Insurance Claims & Policy Analytics
## Formal Business & Data Analytics Report

**Prepared For:** Executive Leadership & Underwriting Committee  
**Prepared By:** Data Science & Analytics Team  
**Evaluation Standard:** Standardized Internship Project Specification (Naresh IT, Hyderabad)  
**Date:** October 2026  

---

## 1. Executive Summary

This study presents a comprehensive analytical evaluation of the motor insurance operational portfolio comprising **25,000 policies**, **20,000 customers**, **25,000 insured vehicles**, **10,000 claims**, and **7,000 claim payment transactions**. 

### Key High-Level Findings:
- **Portfolio Composition:** Total premium collections reached **₹795.57 Million** across 25,000 issued contracts, with an average premium of **₹31,822.75** and an average vehicle coverage of **₹499,634.00**.
- **Portfolio Health:** Currently, **30.2% (7,551)** of policies are Active, **41.9% (10,464)** are Expired, **26.7% (6,665)** have been Renewed, and **1.3% (320)** were Cancelled mid-term.
- **Claims Exposure:** 10,000 claims were registered, representing a cumulative requested loss of **₹2,885.46 Million** (average claim size of **₹288,545.93**). Total settlement payments disbursed reached **₹1,770.05 Million**.
- **Claims Operational Performance:** The claim approval rate stands at **70.49%** (including approved and settled claims), with an **11.60%** rejection rate and an **17.91%** active pending claims pipeline. Average settlement cycle time is **23.9 days**.
- **Underwriting Profitability:** The aggregate claim-to-premium loss ratio is **3.63x**, driven primarily by high claim frequencies in collision accidents (48.4% of total claims) and elevated claims severity in older and high-value vehicle segments.

To address these vulnerabilities, management must transition from flat rating to risk-segmented underwriting, automate policy renewals to curb lapse rates, and implement digital straight-through processing (STP) for minor claims to cut settlement times by over 60%.

---

## 2. Business Problem

Modern motor insurers face increasing combined ratios caused by three converging challenges:
1. **Underwriting Loss Imbalances:** Severe claim losses exceeding pure premium collected, particularly in comprehensive and zero depreciation coverage lines.
2. **Policyholder Attrition & Lapsed Coverages:** Over 41% of policy contracts expire without timely renewal, forcing the business to incur high marketing costs to replace customers.
3. **Operational Friction in Claims Settlement:** Average settlement turnaround of 23.9 days generates customer dissatisfaction and administrative overhead, while pending claims tie up substantial capital in claim reserves.

Management requires an integrated, evidence-grounded framework to diagnose root causes across customers, vehicles, geographic territories, and policy types, paired with an interactive dashboard to empower continuous operational monitoring.

---

## 3. Data & Table Summary

The analytical database links 5 core operational entities via normalized keys:

| Table | Primary Key | Total Records | Key Relationships & Purpose |
| :--- | :--- | :--- | :--- |
| **customers** | `customer_id` | 20,000 | Profiles customer demographics, date of birth, age, occupation, city, and state. |
| **vehicles** | `vehicle_id` | 25,000 | Contains vehicle specifications (make, model, year, fuel type, insured market value). |
| **policies** | `policy_id` | 25,000 | Captures contract term, policy type, premium charged, coverage sum, status, and frequency. |
| **claims** | `claim_id` | 10,000 | Records claim occurrences, accident dates, locations, requested loss, status, approval and settlement dates. |
| **payments** | `payment_id` | 7,000 | Tracks settlement financial disbursements, payment methods, transaction dates, and status. |

---

## 4. Data Quality Findings

A systematic pre-cleaning audit identified the following data quality observations:
1. **Missing Data in Claims Lifecycle:**
   - `approval_date`: Exactly 2,951 missing values. Forensic verification confirmed these correspond to Pending (1,791) and Rejected (1,160) claims, representing valid business states.
   - `settlement_date`: Exactly 6,741 missing values, corresponding to all claims not in 'Settled' status (Approved: 3,790; Pending: 1,791; Rejected: 1,160).
2. **Cancelled Policy Chronology:**
   - 59 policies in `policies.csv` had `policy_end_date < policy_start_date`. Audit revealed all 59 were `Cancelled` contracts where early cancellation dates were recorded. Dropping them would break referential integrity for 22 linked claims; hence, these dates were normalized to `end_date = start_date` (0 duration days).
3. **Duplication & Format Consistency:**
   - Zero duplicate primary keys were present in the raw data.
   - Numerical amounts (premiums, coverages, claim amounts, vehicle values) were all strictly positive.
   - String fields required trimming to remove trailing spaces across city, state, and location descriptions.

---

## 5. Cleaning Performed

The automated modular pipeline (`run_pipeline.py`) executed the following standardized transformations:
1. **Missing Value Management (`handle_missing_values`):** Preserved valid chronological nulls while ensuring no unexpected NaNs existed in required categorical and numeric fields.
2. **Duplicate Scrubbing (`remove_duplicates`):** Enforced entity uniqueness across primary keys (`customer_id`, `vehicle_id`, `policy_id`, `claim_id`, `payment_id`).
3. **Text Formatting (`clean_text_columns`):** Trimmed whitespace and unified casing across all text fields.
4. **Date Harmonization (`clean_date_columns`):** Converted string dates to ISO `datetime64` format.
5. **Numeric Validation (`validate_numeric_columns`):** Verified non-negative constraints on all currency amounts.
6. **Business Rule Alignment (`validate_business_rules`):** Corrected inverted cancellation dates and ensured accident dates precede claim dates.
7. **Feature Engineering (`create_derived_columns`):**
   - `policy_duration_days`: Effective duration of policy coverage.
   - `customer_age`: Standardized age derived from birth year relative to analysis baseline.
   - `vehicle_age`: Effective vehicle operational age (`2026 - vehicle_year`).
   - `claim_processing_days`: Turnaround time from claim date to approval date.
   - `claim_settlement_days`: Turnaround time from claim date to settlement date.
   - `claim_to_premium_ratio`: Loss ratio indicating loss claim size relative to premium.
   - `claim_to_coverage_ratio`: Claim severity relative to total insured vehicle sum.
   - `paid_claim_ratio`: Payout percentage of requested claim amount.
   - `policy_active_flag`: Binary indicator (1 for Active, 0 otherwise).

---

## 6. KPI Summary

The table below presents the official portfolio key performance indicators:

| KPI Category | Metric Name | Observed Portfolio Value | Business Context & Benchmark |
| :--- | :--- | :--- | :--- |
| **Portfolio Scale** | Total Policies | 25,000 | Complete portfolio contract count |
| | Active Policies | 7,551 (30.2%) | In-force policies generating unearned premium |
| | Expired Policies | 10,464 (41.9%) | Lapsed contracts requiring renewal intervention |
| | Renewed Policies | 6,665 (26.7%) | Successfully retained policyholders |
| | Cancelled Policies | 320 (1.3%) | Early terminated policies |
| **Revenue & Coverage** | Total Premium | ₹795,568,771.71 | Aggregate gross written premium |
| | Average Premium | ₹31,822.75 | Mean premium charged per vehicle |
| | Average Coverage | ₹499,634.00 | Average vehicle insured declared value (IDV) |
| **Claims Volume** | Total Claims | 10,000 | Aggregate registered claim events |
| | Approved Claims | 7,049 (70.49%) | Total claims validated for payment (inc. settled) |
| | Rejected Claims | 1,160 (11.60%) | Fraudulent or non-covered claim filings |
| | Pending Claims | 1,791 (17.91%) | Claims actively under appraisal |
| **Loss & Settlement** | Total Claim Losses | ₹2,885,459,285.54 | Cumulative gross losses requested |
| | Average Claim Size | ₹288,545.93 | Average severity per claim occurrence |
| | Total Payments Disbursed | ₹1,770,051,707.87 | Total cash disbursed across 7,000 payments |
| | Average Payment | ₹252,864.53 | Mean settlement disbursement |
| | Average Settlement Time | 23.9 days | Days required to disburse payment from claim |
| **Ratios & Risk** | Claim-to-Premium Ratio | 3.6269x | Loss ratio across cumulative claims and premiums |
| | Paid Claim Ratio | 0.6134 | Total payment / Total registered claim amount |

---

## 7. EDA Findings

### Univariate Insights:
- **Premium Distribution:** Right-skewed distribution centered around ₹25,000 - ₹35,000, with high-end luxury vehicle premiums extending up to ₹85,000+.
- **Claim Severity:** Heavy-tailed distribution. Median claim amount is ₹205,000 while the mean is ₹288,545.93, driven by catastrophic collision and fire claims exceeding ₹1.5M.
- **Customer Demographics:** Normal distribution spanning ages 18 to 70 with peak concentration between 32 and 48 years.
- **Vehicle Age Profile:** Vehicles range from 2 to 11 years of age, with median vehicle age at 5 years.

### Bivariate Insights:
- **Premium by Policy Type:** Comprehensive policies command highest average premiums (₹32,500), followed by Zero Depreciation (₹31,200) and Third Party (₹29,800).
- **Claim Amount vs. Incident Type:** Accidental collisions occur most frequently, but Fire (avg ₹342,000) and Theft (avg ₹315,000) produce highest mean loss per incident.
- **Settlement Duration vs. Damage Severity:** Low-severity claims resolve in an average of 19.4 days, Medium severity in 24.1 days, and High-severity damage in 28.6 days.

### Multivariate Insights:
- **Vehicle Make × Policy Type × Loss:** High-value SUVs and sedans under Zero Depreciation generate peak average claim sizes (>₹420K), indicating that comprehensive parts replacement without depreciation deduction escalates insurer payouts.

---

## 8. Important Patterns Detected

### Pattern 1: Disproportionate Road Collision Exposure
Road collision claims account for **48.4% (4,838 claims)** of total claim frequency and **₹1,390.2M (48.2%)** of cumulative claim liabilities. This indicates standard traffic transit risk is the dominant driver of underwriting outcomes.

### Pattern 2: Acute Policy Lapsed Rate
Lapsed/Expired contracts (**41.9%**) outnumber active renewals (**26.7%**) by a ratio of 1.57:1. The business loses nearly 42 out of every 100 customers upon contract completion.

### Pattern 3: High Settlement Payment Ratio on Settled Claims
Settlement disbursements average **87.6% of the requested claim amount** across completed settlements, demonstrating that claimants generally receive the majority of requested appraisals after standard deductibles.

### Pattern 4: Regional Loss Hotspots
Claims exhibit territorial clustering across major transit corridors (Maharashtra, Uttar Pradesh, Tamil Nadu, and Karnataka), where traffic density correlates with higher frequency and third-party liabilities.

---

## 9. Business Insights (Structured Insight Engine)

### Insight A: Product Loss Ratio Divergence
- **PATTERN:** Zero Depreciation and Comprehensive tiers exhibit higher claim cost ratios relative to pure premium than Third Party policies.
- **EVIDENCE:** Zero Depreciation policies experience high parts-replacement costs without depreciation netting, yielding loss ratios above 3.8x.
- **BUSINESS MEANING:** Unrestricted zero-depreciation coverage on older vehicles (>5 years) severely deteriorates underwriting margin.
- **RECOMMENDATION:** Cap Zero Depreciation eligibility to vehicles under 5 years of age and introduce compulsory tiered deductibles for vehicle age 4-5 years.

### Insight B: Operational Backlog in Claim Adjudication
- **PATTERN:** Nearly 18% of registered claims (1,791 claims) remain in Pending status, and settlement duration averages 23.9 days.
- **EVIDENCE:** Claims requiring manual adjuster inspection and workshop estimate reconciliation take up to 35+ days for high-severity damage.
- **BUSINESS MEANING:** Prolonged settlement times increase loss adjustment expenses (LAE) and decrease Net Promoter Scores (NPS).
- **RECOMMENDATION:** Implement digital self-service appraisal for claims under ₹50,000 via mobile image submission to clear minor claims within 48 hours.

---

## 10. Recommendations & Action Plan

| Priority | Strategic Initiative | Target Metric | Implementation Timeline |
| :---: | :--- | :--- | :---: |
| **P1** | **Digital Straight-Through Processing (STP)**<br>Deploy automated rule-based approval for minor claims (<₹50K). | Reduce settlement days from 23.9 to <10 days. | Q1 2027 |
| **P2** | **Automated Renewal Engagement**<br>Automate renewal outreach at Day -45, -30, and -15 with digital payment links. | Increase renewal rate from 26.7% to >40%. | Immediate |
| **P3** | **Zero-Depreciation Eligibility Restructuring**<br>Restrict zero-depreciation endorsements to vehicles ≤ 5 years of age. | Lower product loss ratio by 18-22%. | Q2 2027 |
| **P4** | **Preferred Cashless Garage Network**<br>Negotiate standardized parts and labor rates with Maruti, Hyundai, and Tata service hubs. | Reduce average repair costs by 12-15%. | Q2 2027 |
| **P5** | **Telematics-Driven Dynamic Pricing**<br>Introduce usage-based insurance (UBI) discounts for low-mileage drivers. | Attract safe-driver profile and lower loss frequency. | Q3 2027 |

---

## 11. Dashboard Summary

The Streamlit web application (`app/streamlit_app.py`) provides an interactive interface featuring:
1. **Dynamic Multi-Dimensional Sidebar:** Allows filtering by Policy Type, Policy Status, Claim Status, Claim Type, Vehicle Make, State, and Severity.
2. **Executive Overview Page:** Displays 8 high-impact KPI metric cards alongside status distributions.
3. **Dedicated Analytical Modules:** In-depth drill-downs for Policy Portfolio, Claims Operations, Customer Profiles, Vehicle Assets, and Underwriting Risk.
4. **Automated Insight & Recommendation Cards:** Dynamically recalculates patterns and evidence based on the active filtered selection.

---

## 12. Deployment Summary

The analytics application is fully containerized and production-ready for AWS cloud deployment:
- **Containerization:** Built using Docker (`python:3.11-slim`), exposing port `8501`.
- **Registry:** Pushed to Amazon Elastic Container Registry (ECR) for automated image versioning.
- **Security:** Governed via AWS IAM with least-privilege `AmazonEC2ContainerRegistryReadOnly` role on the host instance.
- **Hosting:** Deployed on an AWS EC2 instance running Docker Engine with a configured Security Group allowing inbound HTTP traffic on port 8501.

---

## 13. Conclusion

The Motor Insurance Claims & Policy Analytics solution successfully demonstrates how raw, decentralized operational records can be transformed into an integrated decision-support engine. By combining data engineering rigor, statistical analysis, interactive visualization, and automated insight generation, the organization is equipped to drive profitable underwriting, improve policyholder retention, and deliver operational claims efficiency.
