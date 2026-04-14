# Data Warehouse: Concepts, Architecture, and Implementation

This repository contains a comprehensive guide to Data Warehousing, based on the "DTalks-DataEng" presentation. It covers fundamental definitions, architecture, and deep dives into BigQuery internals and optimization.

## Table of Contents
1. [OLTP vs. OLAP](#2-oltp-vs-olap)
2. [Data Warehouse Architecture](#3-data-warehouse-architecture)
3. [BigQuery Internals](#4-bigquery-internals)
4. [Partitioning vs. Clustering](#5-partitioning-vs-clustering)
5. [BigQuery Query Best Practices](#6-bigquery-query-best-practices)
6. [Data Modeling Methodologies](#7-data-modeling-methodologies)

---

## 1. OLTP vs. OLAP
| Feature | OLTP (Transactional) | OLAP (Analytical) |
| :--- | :--- | :--- |
| **Purpose** | Day-to-day operations | Decision support |
| **Query Type** | Simple, fast | Complex aggregations |
| **Data Format** | Normalized (3NF) | Denormalized (Star/Snowflake) |

---

## 2. Data Warehouse Architecture
1. **Source Layer:** Raw data from DBs, APIs, etc.
2. **Staging Area:** Temporary landing zone for cleaning.
3. **DW Layer:** Integrated historical storage.
4. **Data Marts:** Business-specific subsets (Finance, Marketing).
5. **Analytics:** BI and reporting tools.

---

## 3. BigQuery Internals
BigQuery separates storage from compute using three core technologies:
* **Colossus:** Google’s global storage system. Data is stored in the **Capacitor** columnar format.
* **Dremel:** The compute engine that executes queries using a massive tree-structured distribution of "slots" (virtual CPUs).
* **Jupiter:** The high-speed network that allows lightning-fast data transfer between Colossus and Dremel.

---

## 4. Partitioning vs. Clustering
To optimize performance and reduce costs, data should be organized effectively.

### Partitioning
Divides a table into segments called partitions based on a specific column (usually date or integer).
* **Benefit:** BigQuery only scans the partitions that match your filter (**Partition Pruning**).
* **Limit:** Up to 4,000 partitions per table.

### Clustering
Sorts data within partitions based on the values of specific columns (up to 4 columns).
* **Benefit:** Co-locates similar data blocks, improving filter and aggregation efficiency.
* **Best For:** High-cardinality columns (e.g., `user_id`, `tags`).

---

## 5. BigQuery Query Best Practices
* **Avoid `SELECT *`:** Only query the columns you need to minimize data processed.
* **Filter on Partitioned Columns:** Always include the partition key in your `WHERE` clause.
* **Order of Joins:** Place the largest table first. BigQuery broadcasts the smaller (right-side) table to all processing nodes.
* **Handle Data Skew:** Avoid joining on keys with many NULL values or extreme frequency, as it can overwhelm single processing slots.
* **Use Preview:** Use the "Preview" tab in the UI to explore data for free instead of running a query.

---

## 6. Data Modeling Methodologies
### Kimball (Bottom-Up)
* Focus on **Dimensional Modeling** (Star Schema).
* Fast to implement, user-friendly.

### Inmon (Top-Down)
* Focus on **Enterprise Data Warehouse** (3NF).
* Centralized "Single Version of the Truth."

---

### Reference
* **Original Presentation:** [DTalks-DataEng-Data Warehouse](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit?usp=sharing)