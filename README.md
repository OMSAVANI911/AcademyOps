# AcademyOps – Lead-to-Enrollment Management System

## Overview

AcademyOps is a full-stack lead management and enrollment tracking platform developed for EasySkill Career Academy (ECA).

The system is designed to capture leads from multiple marketing channels, track them through a structured admissions pipeline, provide operational visibility through analytics dashboards, and expose business functionality through a modern REST API.

The project demonstrates practical software engineering concepts including:

* Backend API development with FastAPI
* Database abstraction using the Repository Pattern
* Data validation with Pydantic
* Automated testing with Pytest
* Data processing with Pandas
* Dashboard development with Streamlit
* Software architecture and modular design
* ETL-style CSV ingestion and cleaning pipelines

---

# Project Objectives

The primary goals of AcademyOps are:

1. Centralize lead management operations.
2. Track prospective students throughout the enrollment funnel.
3. Maintain clean and validated lead records.
4. Provide operational insights through analytics.
5. Demonstrate industry-standard Python software engineering practices.

---

# Technology Stack

| Category          | Technology        |
| ----------------- | ----------------- |
| Language          | Python 3          |
| Backend Framework | FastAPI           |
| ASGI Server       | Uvicorn           |
| Validation        | Pydantic          |
| Database          | SQLite            |
| ORM               | SQLAlchemy        |
| Analytics         | Pandas            |
| Dashboard         | Streamlit         |
| Testing           | Pytest            |
| API Documentation | Swagger / OpenAPI |
| Version Control   | Git & GitHub      |

---

# Architecture

The application follows a layered architecture.

```text
Client
   │
   ▼
FastAPI REST API
   │
   ▼
Repository Layer
   │
   ▼
SQLAlchemy Models
   │
   ▼
SQLite Database
```

The repository layer isolates business logic from database implementation details, improving maintainability and testability.

---

# Core Features

## Lead Management

### Create Lead

Create a new lead with:

* Name
* Phone Number
* Lead Source
* Pipeline Stage
* Notes

### Retrieve Lead

Retrieve individual lead records using unique identifiers.

### List Leads

View all stored leads with pagination support.

### Update Lead Stage

Move leads through the admissions funnel.

Supported stages:

* New
* Contacted
* Qualified
* Demo
* Enrolled
* Lost

### Duplicate Detection

The system prevents duplicate phone number entries.

---

# Admissions Pipeline

```text
New
 │
 ▼
Contacted
 │
 ▼
Qualified
 │
 ▼
Demo
 │
 ▼
Enrolled

OR

Lost
```

This structure models a realistic student enrollment workflow.

---

# Data Ingestion Pipeline

The platform includes a CSV ingestion workflow.

Capabilities include:

* CSV import
* Data cleaning
* Format standardization
* Invalid record detection
* Quarantine file generation

Corrupted records are automatically redirected into a quarantine dataset for manual review.

---

# Analytics Module

AcademyOps includes analytical reporting powered by Pandas.

Metrics include:

* Total Leads
* Conversion Rates
* Stage Distribution
* Source Performance
* Funnel Health Indicators

---

# Streamlit Dashboard

A Streamlit dashboard provides operational visibility.

Dashboard functionality:

* Funnel analytics
* Lead statistics
* Source breakdowns
* CSV import results
* Operational summaries

---

# REST API

## Available Endpoints

### Get Lead

```http
GET /api/v1/leads/{lead_id}
```

### List Leads

```http
GET /api/v1/leads
```

### Create Lead

```http
POST /api/v1/leads
```

### Update Lead Stage

```http
PATCH /api/v1/leads/{lead_id}/stage
```

### Classify Message

```http
POST /api/v1/leads/{lead_id}/message
```

---

# API Documentation

After starting the application:

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Project Structure

```text
academyops/
│
├── data/
│   ├── messy_leads.csv
│   ├── quarantine.csv
│   └── source_chart.png
│
├── src/
│   ├── api.py
│   ├── analytics.py
│   ├── classifier.py
│   ├── database.py
│   ├── importer.py
│   ├── repository.py
│   ├── schemas.py
│   └── templates/
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/OMSAVANI911/AcademyOps.git
cd AcademyOps
```

## Create Virtual Environment

```bash
python -m venv venv
```

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Backend

```bash
uvicorn src.api:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

---

# Running Tests

```bash
PYTHONPATH=. pytest -v
```

Expected result:

```text
3 passed
```

---

# Running the Dashboard

```bash
streamlit run src/analytics.py
```

---

# Work Package Development Timeline

## WP-00 — Environment Setup

* Git repository initialization
* Virtual environment setup
* Project structure creation

## WP-01 — Database & Repository Pattern

* SQLite schema design
* Repository abstraction layer
* CRUD operations

## WP-02 — Data Ingestion Pipeline

* CSV import workflow
* Data cleaning
* Quarantine handling

## WP-03 — REST API

* Initial backend implementation
* Endpoint design

## WP-04 — Automated Testing

* Pytest integration
* API validation testing

## WP-05 — Data Analytics

* Funnel metrics
* Source performance analysis

## WP-06 — Operations Dashboard

* Streamlit dashboard implementation

## WP-07 — FastAPI Migration

* Migration from Flask to FastAPI
* Pydantic schema validation
* Swagger/OpenAPI integration

---

# Testing

Current automated coverage includes:

* Lead creation
* Lead retrieval
* Repository exception handling

Implemented using Pytest.

---

# Future Improvements

Potential enhancements:

* PostgreSQL deployment
* Authentication and authorization
* Docker containerization
* CI/CD pipelines
* Advanced analytics
* Role-based access control
* Cloud deployment

---

# Author

Om Savani

Capstone Project – EasySkill Career Academy

Built using Python, FastAPI, SQLAlchemy, Pandas, Streamlit, and Pytest.
