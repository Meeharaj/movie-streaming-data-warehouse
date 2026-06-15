
## 🎬 Project Overview: End-to-End Movie Warehouse & Streaming Intelligence
📌 Executive Summary
In the digital entertainment industry, media executives and content acquisition teams struggle to analyze library performance due to fragmented data across multiple competing streaming platforms (Netflix, Prime Video, Apple TV+, etc.). Critical metadata—such as genres, directors, and audience vs. critic ratings—is often trapped in unformatted, multi-value text arrays inside flat files, preventing scalable business intelligence.

This project bridges that gap by building an end-to-end data engineering and analytics solution. The pipeline ingests a raw registry of the top 500 cinematic releases of all time, cleanses and normalizes the attributes using Python, architectures a high-performance lowercase Star Schema Data Warehouse in Microsoft SQL Server, and delivers platform-style market intelligence through an immersive, dark-mode Power BI Executive Dashboard.


## 📊 Live Dashboard Preview

### 1. Executive Insights Matrix (Midnight Theatre UI)
*Featuring a premium streaming-service dark theme, glass morphism card components, and advanced market-share tracking charts.*

<img width="1341" height="736" alt="Page Executive Insights" src="https://github.com/user-attachments/assets/e83f6d64-07cf-477d-8d04-e9cc80f1684a" />



### 2. Algorithmic Deep Dive & Platform Stream
*An interactive diagnostic canvas mapping audience vs. critic sentiment across a custom matrix scatter plot. This view allows media stakeholders to instantly isolate "Cult Classics" (high audience, lower critic scores) from "Critic Darlings" across different streaming ecosystems..*

<img width="1317" height="735" alt="Sentimental and Platform Deep-Dive" src="https://github.com/user-attachments/assets/db26e846-bb0b-4673-a7d1-2540da189896" />


---

## 🎯 Key Project Insights & Business Impact
* **Platform Library Dominance:** Discovered which major streaming providers (Netflix, Prime Video, iTunes) currently license the highest market share of top-tier cinematic titles.
* **The "Boutique Curator" Advantage:** Isolated premium content hubs that maintain low raw movie volume but boast an exceptionally high average custom score matrix.
* **Cinematic Era Fluctuations:** Tracked rating movements over a multi-decade timeline, identifying which historic eras maintain the highest audience and critic consensus agreements.

---

## 🛠️ Tech Stack & Architecture
* **Data Layer:** Python 3.x, pandas, SQLAlchemy, pyodbc
* **Warehouse Engine:** Microsoft SQL Server (T-SQL)
* **Visualization Layer:** Power BI Desktop (Advanced DAX Modelling)

### The Data Architecture Pipeline
1. **Extraction:** Raw flat-file CSV containing multi-value arrays (comma-separated strings) ingested into a pandas dataframe.
2. **Transformation:** Replaced null values with median weights, cleaned trailing text spaces, isolated lists via exploding mechanisms, and forced the entire structural schema to standard lowercase formatting.
3. **Staging & Loading:** Bulk-loaded clean data into a relational SQL Engine with explicit variable definitions to prevent text truncation bugs.
4. **Data Modeling:** Hardened structural relationships using explicit Primary/Foreign Key declarations and Non-Clustered indexing.

---

## 📐 Data Warehouse Schema (Optimized Star Schema)

The architecture splits computational logic out of the core data table into highly queryable bridges to optimize Power BI data traversal lines:

* **`fact_movie_ratings` (Fact Table):** Tracks numerical scores, ranks, and voter footprints (`imdbid`, `rank`, `custom_score`, `critic_rating_rt`, `audience_rating`, `imdb_votes`).
* **`dim_movies` (Core Dimension):** Contains unique identity attributes (`imdbid`, `title`, `year`, `language`, `production`, `streaming_on`).
* **`dim_genres` (Bridge Dimension):** Holds individual exploded genre records linked back via (`imdbid`, `genre`).
* **`dim_directors` (Bridge Dimension):** Holds individual exploded director records linked back via (`imdbid`, `director`).

---
