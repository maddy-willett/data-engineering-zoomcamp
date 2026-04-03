# Data Engineering Zoomcamp 2026

![Status](https://img.shields.io/badge/Zoomcamp-Week%201%20Complete-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Terraform](https://img.shields.io/badge/Terraform-In%20Progress-orange)

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

---
