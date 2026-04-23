# 🌄 West Virginia Economic Analysis  
### Data Pipeline • Database • Interactive Dashboard

---

## 📌 Project Overview

This project is a **production-style rebuild** of a previously completed team-based economic analysis of West Virginia’s economy.

The original team project developed an initial analytical framework exploring workforce trends, industry structure, and business activity using multiple public datasets.

This version re-engineers and extends that work into a structured, production-style system with:

- Modular Python data pipeline  
- PostgreSQL database layer  
- Reusable analytical functions  
- Interactive Streamlit dashboard  

The goal is to demonstrate how an existing analytical project can be transformed into a scalable, production-ready data application.

---

## 🎯 Objectives

- Build a modular data pipeline using Python  
- Store and manage datasets in PostgreSQL  
- Standardize analytical logic across datasets  
- Develop an interactive Streamlit dashboard  
- Translate raw data into clear, explainable insights  

---

## 🧰 Tech Stack

### ⚙️ Data Engineering & Processing
![Python](https://img.shields.io/badge/Python-Data_Pipeline-yellow?style=flat&logo=python&logoColor=yellow)
![Pandas](https://img.shields.io/badge/Pandas-Data_Transformation-yellow?style=flat&logo=pandas&logoColor=white)
![ETL](https://img.shields.io/badge/ETL-Pipeline_Design-yellow?style=flat)

### 🗄️ Data Storage & Querying
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=flat&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Data_Querying-4169E1?style=flat&logo=microsoftsqlserver&logoColor=white)

### 📊 Visualization & Analytics
![Streamlit](https://img.shields.io/badge/Streamlit-Data_App-red?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-red?style=flat)
![Time Series](https://img.shields.io/badge/Time_Series-Analysis-red?style=flat)

### 🛠️ Tools & Environment
![VS Code](https://img.shields.io/badge/VS_Code-Development_Environment-orange?style=flat&logo=visual-studio-code&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Data_Exploration-orange?style=flat&logo=jupyter&logoColor=orange)
![Git](https://img.shields.io/badge/Git-Version_Control-orange?style=flat&logo=git&logoColor=orange)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github&logoColor=white)

---

## 🏗️ Project Architecture

This project follows a structured ETL data workflow:

1. **Extract** – Collect raw data from:
   - Bureau of Labor Statistics (BLS)  
   - Bureau of Economic Analysis (BEA)  
   - West Virginia Secretary of State (WVSOS)  

2. **Transform** – Clean and standardize datasets using Python (Pandas)

3. **Load** – Store processed data in PostgreSQL

4. **Analyze** – Apply reusable analytical logic (growth, share, trends)

5. **Visualize** – Deliver insights through a Streamlit dashboard

---

## 📊 Dashboard Features

### 🔍 Industry Analysis
- Compare industries by employment and GDP
- Identify growth vs decline using multi-year analysis
- Visualize performance using scatter plots with quadrant analysis

### 📈 Economic Trends
- Track statewide trends in:
  - Employment  
  - Labor Force  
  - Labor Force Participation Rate (LFPR)  
  - Unemployment Rate  
- Analyze long-term labor market dynamics

### 🏢 Business Dynamics
- Explore business formation and termination trends  
- Measure net business growth across industries  
- Identify sectors with expanding or contracting activity  

---

## 🧠 Key Insights (Example)

- Employment is concentrated in a small number of dominant industries  
- Labor force participation shows long-term structural trends  
- Some industries exhibit strong employment growth but weaker GDP performance  
- Business formation varies significantly across sectors  

---

## 📈 Project Evolution

This project builds directly on a previously completed team-based economic analysis of West Virginia’s economy.

Original project:  
[West Virginia Economic Trends – Generation WV NewForce Insights Team Project](https://wvinsights.info/)

It evolved from a notebook-based analysis into a structured, production-style application with:

- Modular code organization (`utils`, `sql`, `pages`)  
- Reusable analytical logic (growth, share, performance metrics)  
- Centralized data transformations  
- Interactive Streamlit dashboard  

This transition reflects a shift from exploratory analysis → production-ready analytics system.  

---

## 🚀 Status

🟢 Complete — core pipeline, database, and dashboard are fully functional  

---

## 📌 Future Improvements

- [ ] Deploy Streamlit app for public access  
- [ ] Add geographic (county-level) analysis  
- [ ] Expand industry-level forecasting  
- [ ] Integrate additional economic indicators  

---