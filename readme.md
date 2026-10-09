# Motor Insurance Claims & Policy Analytics

> **Standardized Internship Project Specification & Analytical Solution**  
> *Developed for Naresh IT, Hyderabad — Directed by Mr. Ravi Varma (Ex-IBM Technical Trainer)*

---

## 1. Project Title
**Motor Insurance Claims & Policy Analytics**: An Enterprise-Grade End-to-End Data Analytics, Risk Modeling, Streamlit Dashboard, and AWS Cloud Deployment Pipeline.

---

## 2. Business Scenario
You are operating as a Senior Data & Business Analyst for a motor insurance provider managing an active portfolio of 25,000 policy contracts across 20,000 individual policyholders and their insured vehicles. Management requires a robust, reproducible analytical engine to monitor policy lifecycle states, premium cash flows, claims frequency, severity concentrations, settlement operational cycle times, customer demographic profiles, and vehicle loss ratios.

---

## 3. Business Problem
Motor insurance operations face complex multi-factor underwriting risks:
- High volume of policy expirations leading to churn and customer attrition.
- Elevated claim loss ratios across select policy types and vehicle makes that threaten underwriting profitability.
- Operational backlogs in claim settlement timelines (averaging 23.9 days) and high pending claims volumes.
- Need for evidence-grounded risk segmentation across geographic territories, vehicle age brackets, and driver demographics.

---

## 4. Objectives
1. Build a modular Python pipeline to load, validate, clean, and engineer derived actuarial features across 5 relational tables.
2. Formulate essential insurance KPIs and statistical measures of central tendency, dispersion, and loss ratios.
3. Conduct in-depth exploratory data analysis (EDA) across univariate, bivariate, and multivariate dimensions.
4. Uncover empirical risk patterns and translate them into structured business insights and strategic recommendations.
5. Deliver an interactive Streamlit frontend with dynamic sidebar filters that update KPI metrics, charts, and insight cards in real time.
6. Enforce production standards: unit testing with pytest/unittest, structured logging, containerization via Docker, and production deployment architecture on AWS (ECR, IAM, EC2).

---

## 5. Technology Stack
- **Core Languages & Data Manipulation:** Python 3.11, Pandas, NumPy, Scipy
- **Data Visualization & Analytics:** Matplotlib, Seaborn, Jupyter Notebook
- **Frontend Dashboard:** Streamlit
- **Quality Engineering & Testing:** Pytest, Unittest, Python Logging
- **DevOps & Containerization:** Git, Docker, Dockerfile
- **Cloud Infrastructure & Deployment:** AWS ECR (Elastic Container Registry), AWS IAM (Least-Privilege Roles), AWS EC2 (Elastic Compute Cloud)

---

## 6. Data Model & Table Relationships
The schema comprises five normalized relational tables:

```
customers (1) ──────────< policies (M) >────────── (1) vehicles
   │                           │
   │                           │
   └──(1)─────────────────────>└──(M) claims
                                       │
                                       └──(M) payments
```

### Relational Schema:
1. **customers** (`customer_id` [PK], `customer_name`, `gender`, `date_of_birth`, `age`, `city`, `state`, `occupation`)
2. **vehicles** (`vehicle_id` [PK], `customer_id` [FK], `vehicle_type`, `vehicle_make`, `vehicle_model`, `vehicle_year`, `fuel_type`, `vehicle_value`)
3. **policies** (`policy_id` [PK], `customer_id` [FK], `vehicle_id` [FK], `policy_start_date`, `policy_end_date`, `policy_type`, `premium_amount`, `coverage_amount`, `policy_status`, `payment_frequency`)
4. **claims** (`claim_id` [PK], `policy_id` [FK], `customer_id` [FK], `claim_date`, `accident_date`, `claim_type`, `accident_location`, `claim_amount`, `claim_status`, `approval_date`, `settlement_date`, `damage_severity`)
5. **payments** (`payment_id` [PK], `claim_id` [FK], `policy_id` [FK], `payment_date`, `payment_amount`, `payment_status`, `payment_method`)

---

## 7. Project Structure
The repository strictly adheres to the standardized folder convention:

```
motor_insurance_analytics/
│
├── data/
│   ├── raw/                           # Raw immutable operational CSVs
│   │   ├── customers.csv
│   │   ├── policies.csv
│   │   ├── vehicles.csv
│   │   ├── claims.csv
│   │   └── payments.csv
│   │
│   └── cleaned/                       # Business-ready, cleaned & feature-engineered CSVs
│       ├── customers_cleaned.csv
│       ├── policies_cleaned.csv
│       ├── vehicles_cleaned.csv
│       ├── claims_cleaned.csv
│       └── payments_cleaned.csv
│
├── notebooks/
│   └── insurance_analysis.ipynb       # 19-section end-to-end analytical study
│
├── src/
│   ├── __init__.py                    # Package initializer & submodule exports
│   ├── data_loader.py                 # File validation & batch loading
│   ├── validation.py                  # Schema, domain & relational integrity
│   ├── data_cleaner.py                # Cleaning pipeline & derived feature creation
│   ├── insurance_analysis.py          # Standardized KPIs & segmentation analysis
│   ├── visualization.py               # 18 standard visualization functions
│   ├── insights.py                    # Structured pattern & insight engine
│   └── logger.py                      # Rotating file & console logging
│
├── app/
│   └── streamlit_app.py               # Multi-page interactive Streamlit dashboard
│
├── reports/
│   └── business_report.md             # Formal 13-section business report
│
├── tests/
│   ├── test_pipeline.py               # Pipeline & cleaner unit tests
│   ├── test_analysis.py               # KPI & ratio analytical tests
│   └── test_validation.py             # Schema & foreign-key validation tests
│
├── logs/
│   └── pipeline.log                   # Runtime execution log records
│
├── run_pipeline.py                    # Pipeline entry point CLI script
├── requirements.txt                   # Production package dependencies
├── Dockerfile                         # Production multi-stage Docker build
├── .dockerignore                      # Build context exclusions
├── .gitignore                         # Version control ignore definitions
└── README.md                          # Comprehensive technical documentation
```

---

## 8. Installation

### Prerequisites
- Python 3.9+ (Python 3.11 recommended)
- Git
- Docker (optional for containerized deployment)

### Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/motor-insurance-analytics.git
cd motor-insurance-analytics

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 9. Data Cleaning Pipeline
Execute the automated data cleaning and transformation pipeline:

```bash
python run_pipeline.py
```

### Pipeline Steps:
1. `load_all_data()`: Reads raw tables with path verification.
2. `validate_all_tables()`: Enforces required columns, PK uniqueness, valid numeric bounds, and relational referential integrity.
3. `clean_data()`:
   - `handle_missing_values()`: Preserves valid business absences (`approval_date`, `settlement_date`).
   - `remove_duplicates()`: Drops duplicate rows and ensures PK singularity.
   - `clean_text_columns()`: Strips whitespace and standardizes casing.
   - `clean_date_columns()`: Converts string dates to `datetime64`.
   - `validate_numeric_columns()`: Verifies non-negative constraints.
   - `validate_business_rules()`: Corrects date chronology and aligns cancellation dates.
   - `create_derived_columns()`: Computes policy duration, vehicle age, settlement cycle time, and claim-to-premium loss ratios.
4. `save_cleaned_data()`: Exports business-ready datasets to `data/cleaned/`.

---

## 10. How to Run Tests
Run the automated test suite covering pipeline, validation, and analytics functions:

```bash
# Execute using unittest runner
python3 -m unittest discover -s tests -p "test_*.py" -v

# Or execute using pytest (if installed)
pytest tests/ -v
```

All 16 test cases verify schema enforcement, duplicate removal, derived metric math, and relational integrity.

---

## 11. How to Run Streamlit Locally
Launch the interactive 7-page dashboard locally:

```bash
streamlit run app/streamlit_app.py
```
Open your browser at `http://localhost:8501`.

---

## 12. Docker Instructions

### Build the Docker Image
```bash
docker build -t motor-insurance-analytics .
```

### Run Locally via Docker
```bash
docker run -d -p 8501:8501 --name motor_insurance_app motor-insurance-analytics
```
Access the application at `http://localhost:8501`. Verify container logs:
```bash
docker logs -f motor_insurance_app
```

---

## 13. AWS Deployment Overview

```
Local Codebase ──> Docker Build ──> Amazon ECR ──> AWS EC2 (Instance) ──> Public Browser (:8501)
```

1. **Amazon ECR (Registry):**
   - Create private ECR repository: `aws ecr create-repository --repository-name motor-insurance-analytics`
   - Authenticate Docker: `aws ecr get-login-password | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com`
   - Tag and push:
     ```bash
     docker tag motor-insurance-analytics:latest <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/motor-insurance-analytics:latest
     docker push <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/motor-insurance-analytics:latest
     ```
2. **AWS IAM (Security):**
   - Attach `AmazonEC2ContainerRegistryReadOnly` policy to an IAM Role for EC2.
   - Never embed AWS secret keys in Docker images or source code.
3. **AWS EC2 (Hosting):**
   - Launch Ubuntu t3.medium instance.
   - Configure Security Group: Inbound TCP Port 8501 (Custom) and Port 22 (SSH).
   - Install Docker on EC2, pull image from ECR, and execute:
     ```bash
     docker run -d -p 8501:8501 --restart always <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/motor-insurance-analytics:latest
     ```

---

## 14. Key KPIs

| Key Performance Indicator | Portfolio Value | Description / Formula |
| :--- | :--- | :--- |
| **Total Policies** | 25,000 | Total unique policies issued |
| **Active Policies** | 7,551 (30.2%) | In-force policies generating unearned premium |
| **Expired Policies** | 10,464 (41.9%) | Lapsed contracts requiring renewal intervention |
| **Renewed Policies** | 6,665 (26.7%) | Successfully retained policyholders |
| **Cancelled Policies** | 320 (1.3%) | Early terminated policies |
| **Total Premium Collected** | ₹795,568,771.71 | Sum of premium collected across all policies |
| **Average Premium** | ₹31,822.75 | Mean premium charged per vehicle |
| **Average Coverage** | ₹499,634.00 | Average vehicle insured declared value (IDV) |
| **Total Claims Registered** | 10,000 | Number of registered insurance claims |
| **Total Claim Amount** | ₹2,885,459,285.54 | Aggregate claim loss requested |
| **Average Claim Size** | ₹288,545.93 | Average severity per claim occurrence |
| **Claim Approval Rate** | 70.49% | Approved & Settled claims / Total claims |
| **Claim Rejection Rate** | 11.60% | Claims denied coverage |
| **Average Settlement Days**| 23.9 days | Mean duration from claim to settlement |
| **Total Settlement Payout**| ₹1,770,051,707.87 | Total amount disbursed to claimants |
| **Claim-to-Premium Ratio** | 3.6269x | Total Claim Amount / Total Premium |
| **Paid Claim Ratio** | 0.6134 | Total payment / Total registered claim amount |

---

## 15. Business Questions Answered
1. **Policy Status Breakdown:** Active: 7,551 (30.2%), Expired: 10,464 (41.9%), Renewed: 6,665 (26.7%), Cancelled: 320 (1.3%).
2. **Top Premium Generator:** Comprehensive policies generate ₹480M+ (60.3% of total portfolio premium).
3. **Claims Resolution Pipeline:** 10,000 claims total: 3,790 Approved awaiting payment, 3,259 Settled, 1,791 Pending appraisal, 1,160 Rejected.
4. **Claim Severity Drivers:** Fire and Theft incidents show highest average claim severity (~₹380K - ₹450K) despite lower volume compared to collision accidents.
5. **Operational Settlement Speed:** Completed claim settlements take 23.9 days on average; low-severity claims take 19.4 days whereas high-severity claims require 28.6 days.
6. **Manufacturer Claim Distribution:** Maruti Suzuki (37.9%) and Hyundai (26.6%) account for the majority of claim occurrences, directly aligned with vehicle market share.

---

## 16. Important Insights

### Insight 1: Road Collision Dominance
- **Pattern:** Road collision claims account for 48.4% of total claim frequency (4,838 claims) and ₹1,390M in requested liabilities.
- **Evidence:** Accidental damage claims outnumber the next largest category (Third Party) by more than 2.3x.
- **Business Meaning:** Driving behavior and daily road exposure are the primary drivers of underwriting volatility.
- **Recommendation:** Introduce telematics-enabled driving scoring with premium discounts for low-mileage and safe drivers.

### Insight 2: Renewal Churn Hazard
- **Pattern:** Expired policies (41.9%) substantially exceed renewals (26.7%).
- **Evidence:** 10,464 policies lapsed versus 6,665 renewals.
- **Business Meaning:** High lapse rate incurs heavy customer replacement acquisition costs and suppresses portfolio growth.
- **Recommendation:** Deploy automated renewal engagement funnels starting 45 and 15 days prior to expiration with loyalty No-Claim Bonus (NCB) guarantees.

### Insight 3: Loss Ratio Pressure on Zero Depreciation & Comprehensive
- **Pattern:** Product loss ratios indicate high claim frequency relative to collected premium.
- **Evidence:** Aggregate claim-to-premium ratio reaches 3.63x overall across historical observation periods.
- **Business Meaning:** Underpricing vehicle risk or inadequate deductibles threatens underwriting profitability.
- **Recommendation:** Implement stricter pre-policy vehicle inspections, raise mandatory deductibles on high-end luxury models, and segment rates by vehicle age.

---

## 17. Recommendations
1. **Operational Modernization (Fast-Track Claims):** Implement digital Straight-Through Processing (STP) with AI image validation for claims below ₹50,000 to compress cycle time from 24 days to under 7 days.
2. **Underwriting Discipline:** Restructure rating tables to price for vehicle age and geographic risk rather than flat demographic pricing.
3. **Preferred Garage Partnerships:** Contract agreed labor and spare-part pricing with certified Maruti, Hyundai, and Tata workshop networks to contain severity inflation.
4. **Renewal Automation:** Automate digital renewal payment links across WhatsApp and SMS to lift portfolio renewal rates from 26.7% to >45%.

---

## 18. Live Application Deployment
- **Local Endpoint:** `http://localhost:8501`
- **Docker Container:** `motor-insurance-analytics:latest`
- **AWS Live URL:** `http://ec2-xx-xxx-xxx-xx.compute-1.amazonaws.com:8501` *(Deployed via Amazon ECR + EC2 Docker Engine)*
