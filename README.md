# Data Engineering Zoomcamp 2026

![Status](https://img.shields.io/badge/Zoomcamp-Week%202%20Progress-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Terraform](https://img.shields.io/badge/Terraform-Fundamentals%20Complete-brightgreen)
![Kestra](https://img.shields.io/badge/Kestra-In%20Progress-orange)

## My Journey
I am participating in the Data Engineering Zoomcamp because I want to transition from data analysis to building robust data infrastructure. I enjoy the world of programming / development and am on a continuous journey of learning and building as I go! My goal is to move beyond local scripts and learn how to build production-grade pipelines in the cloud.

---

## Tech Stack & Learning Notes

### Docker
**What it is:** A tool that "wraps" software in a container, including everything it needs to run (libraries, settings, etc.).
**Key takeaway:** I used Docker to run **Postgres** and **pgAdmin** without manual installation. This ensures my database environment is identical every time I start it up. 
* *Pro-tip:* Using **Docker Compose** allowed me to manage both the database and the UI (pgAdmin) as a single unit. 

### Terraform
**What it is:** "Infrastructure as Code" (IaC). Instead of clicking buttons in a cloud console, you write a script that "builds" your servers, buckets, and databases.
**Key takeaway:** It provides a blueprint of my infrastructure that is version-controlled and easily reproducible.

### Python & `uv`
**What it is:** Python is the primary language for data manipulation. `uv` is a modern, high-speed package manager that replaces standard `pip`.
**Key takeaway:** I used Python to automate the "ETL" (Extract, Transform, Load) process—pulling raw CSV data from the web and pushing it into SQL.

### Postgres
**What is it:** A powerful, open-source relational database (SQL) that serves as the "Warehouse" or storage layer for structured data.
**Key takeaway:** I used Postgres to store the cleaned data, allowing me to run complex SQL queries and ensure data integrity through schemas, primary keys, and relations that simple CSV/Parquet files can't provide.

### Kestra 
**What is it:** A modern orchestration platform that coordinates the flow of data between my Python scripts, the `uv` environment, and the Postgres database.
**Key takeaway:** I used Kestra to automate the entire workflow; it acts as the "conductor," triggering the Python scripts on a schedule, managing the environment, and ensuring the data lands in Postgres without manual intervention.

---
