# AcademyOps — Lead-to-Enrollment Management System

AcademyOps is a robust lead-to-enrollment management backend built for EasySkill Career Academy (ECA). It captures leads from marketing channels, tracks them through a defined sales pipeline, and provides data-driven analytics on funnel performance.

## 🏗 Tech Stack
* **Backend Engine:** FastAPI & Uvicorn (Migrated from Flask)
* **Data Validation:** Pydantic
* **Database:** SQLite3 (Implemented via the Repository Pattern)
* **Data Pipeline & Analytics:** Python & Pandas
* **Dashboard:** Streamlit
* **Testing:** Pytest

---

## 🚀 Project Status & Work Packages (WP)

This project was built iteratively. Below is the complete development timeline and feature set:

* **WP-00: Environment Setup** * Initialized the Git repository, configured the virtual environment, and established project architecture.
* **WP-01: Database & Repository Pattern** * Designed the SQLite schema and built the `LeadRepository` class to handle secure database transactions (CRUD operations).
* **WP-02: Data Ingestion Pipeline** * Engineered a custom CSV importer that cleans raw marketing data, standardizes formats, and automatically routes corrupted rows into a quarantine file.
* **WP-03: REST API Implementation** * Built the initial web framework to expose database operations over HTTP endpoints.
* **WP-04: Automated Testing Suite** * Developed a comprehensive Pytest suite to serve as an automated health inspector, validating endpoint logic and database integrity.
* **WP-05: Data Science & Analytics** * Integrated Pandas to calculate pipeline conversion rates, stage distributions, and lead source metrics.
* **WP-06: Operations Dashboard** * Deployed a Streamlit frontend interface allowing stakeholders to visualize funnel metrics and CSV ingestion results in real-time.
* **WP-07: FastAPI Enterprise Migration** * Re-platformed the backend from Flask to FastAPI, implementing strict data validation with Pydantic `BaseModel` schemas and auto-generating interactive OpenAPI (Swagger) documentation.

---

## ⚙️ Setup Instructions

To run this project locally, follow these precise configuration steps:

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd academyops
# AcademyOps v1.0

[cite_start]AcademyOps is a lead-to-enrollment management system for EasySkill Career Academy (ECA)[cite: 12].

## Architecture

The system follows a modular architecture:
* [cite_start]**Backend**: FastAPI with PostgreSQL persistence[cite: 414, 423].
* [cite_start]**Intelligence**: Rule-based intent classification[cite: 484].
* [cite_start]**Analytics/Dashboard**: Streamlit-based operations view[cite: 362].

## Setup & Run
1. [cite_start]Clone the repository[cite: 517].
2. Install dependencies: `pip install -r requirements.txt`.
3. [cite_start]Initialize the database: `python -c "from src import database; database.init_db()"`.
4. [cite_start]Run the API: `uvicorn api:app --reload`[cite: 529].
5. [cite_start]Run the dashboard: `streamlit run src/dashboard.py`[cite: 408].

## Testing
[cite_start]Run the full test suite with: `pytest`[cite: 526].
