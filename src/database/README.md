# Database Module – WV Economic Insights Project V2

This folder contains all database-related components for the `wv_insights` PostgreSQL database.

It serves as the central source of truth for:
- Database schema definitions
- Connection utilities
- SQL query definitions
- Future migrations and database maintenance scripts

---

## 🗄️ Database Overview

The project uses a PostgreSQL database named: ***wv_insights***

### Core Tables

All tables are designed for analytical joins on:
- `year`
- `industry` (where applicable)

#### Tables:
- `bls_employment`
- `bls_unemployment`
- `wvsos_yearly`
- `bea_gdp`

---

## 📊 Schema Management

All table creation scripts are stored in: ***schemas.sql***

This file contains:
- CREATE TABLE statements
- Primary structure definitions
- Data types and constraints

⚠️ Important:
Schema definitions are separated from data loading logic to maintain a clean ETL architecture.

---

## 🔌 Database Connection

Database connection utilities will be implemented in: ***db_connection.py***

This module will:
- Create a reusable SQLAlchemy engine
- Centralize connection configuration
- Support all ETL load scripts

---

## 📥 Data Loading

Data ingestion is handled in: ***src/data_pipeline/load/***

This layer uses pandas + SQLAlchemy to:
- Load cleaned CSV data
- Insert into PostgreSQL tables
- Validate row counts and schema consistency

---

## 🧱 Design Principles

This database layer follows:

- **Separation of concerns** (schema vs ETL vs queries)
- **DRY principles** (reusable connection + loaders)
- **Analytical optimization** (year + industry alignment)
- **Reproducibility** (CSV → pandas → SQL pipeline)

---

## 🚀 Next Steps

1. Implement `db_connection.py` using SQLAlchemy
2. Build reusable ETL loader functions
3. Load first dataset (BLS Employment)
4. Validate with SQL queries

---

## 📌 Notes

This database is designed for analytical workloads, not transactional use. It prioritizes:
- query performance for joins
- consistency across datasets
- simplicity of ETL pipelines
