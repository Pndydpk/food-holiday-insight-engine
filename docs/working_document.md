FOODLENS
A decision intelligence engine for food merchants that detects early food trends from social buzz and converts them into actionable campaign recommendations (what to promote, when, where, and with what risk).

✅ Setup Completed (till now) — REGULARIZED

Created GitHub repository for project.

Added README.md, LICENSE, and .gitignore.

Finalized project vision: FoodLens — Food Holiday Insight Engine (data → inference engine → insights → dashboard → merchants).

Agreed on project-first, learn-along-the-way approach.

Attempted web scraping (Playwright, Selenium, Requests).

Took an engineering decision to switch from unreliable scraping to static, authoritative food holiday dataset.

Built full data engineering pipeline handling millions of records.

Updated core product goal: Shifted focus from “dashboard-first” to “inference engine-first (decision intelligence for merchants).”

📅 Learning & Project Timeline — REALIGNED STATUS
Phase 1: Data Collection (09/06/2025 – 09/27/2025)

Learn Python basics for scraping (requests, BeautifulSoup, Selenium).

Attempt real-world scraping (Playwright, Selenium).

Evaluate scraping reliability & failures.

Switch to static curated dataset for food holidays.

Load Uber Eats menu dataset (millions of rows).

✅ Phase 1 completed (with real-world tradeoff decision).

Phase 2: Data Storage (09/28/2025 – 10/11/2025)

Use SQL (SQLite) for structured storage.

Store Uber Eats menus in relational DB.

Store food holidays in separate DB.

Migrate to PostgreSQL (planned later).

Optional NoSQL (MongoDB) later.

🟡 Phase 2 partially complete (SQLite done, Postgres later).

Phase 3: Data Processing (10/12/2025 – 12/16/2025)

Pandas & NumPy for large-scale processing.

Built ETL-style scripts.

Implemented chunk-based processing.

Generated ~76M holiday–menu matches.

Analytics aggregation (holiday popularity, top dishes per holiday).

🟡 Phase 3 processing done, analytics foundation complete.

Phase 4: API Development (12/17/2025 – 12/21/2025)

FastAPI backend.

Serve analytics results via API.

Connected backend to React frontend.

✅ Phase 4 completed (API + frontend integration MVP).

Phase 5: Frontend + Dashboard (12/19/2025 – 12/21/2025)

Interactive dashboard (filters, KPIs).

React-based web UI.

🟡 Phase 5 MVP completed (basic UI + real data flow).

Phase 6: Intelligence Layer (Jan 2026 – Feb 2026)

Pivoted focus to Inference Engine (decision intelligence).

Built Baseline, Momentum, Confidence, Action Window services.

Implemented /pulse/trends API (mock social pipeline).

✅ Phase 6 Inference Engine v1 completed.

Phase 7: Deployment (Planned)

Docker.

Cloud deployment.

Monitoring.

⏳ Planned.

🧾 Daily Log — REGULARIZED
Date: 2025-09-06

Learnt: How to properly structure a GitHub project for a long-term data engineering project.
Built: Created repo with README, LICENSE, .gitignore.
Blockers: None.
Next: Start data sourcing via web scraping.

Date: 2025-09-13

Learnt: How modern websites load data via APIs (Playwright basics).
Built: Ran Playwright scraper; captured JSON endpoints.
Blockers: Data persistence unclear; scraping complexity high.
Next: Improve scraping reliability.

Date: 2025-09-24

Learnt: Importance of documentation and planning.
Built: Drafted working_document.md and roadmap.
Blockers: None.
Next: Finalize repo structure and data flow.

Date: 2025-10-15

Learnt: Limitations of scraping at scale (SSL, JS-heavy pages, blocking).
Built: Tried Requests, Selenium, BeautifulSoup.
Blockers: Incomplete/zero data.
Next: Explore alternative data sources.

Date: 2025-11-06

Learnt: When curated datasets beat scraping in production.
Built: Loaded static food holidays CSV; wrote loader.
Blockers: Encoding issues.
Next: Normalize holiday dataset.

Date: 2025-11-20

Learnt: Pandas cleaning pitfalls.
Built: Fixed loader; validated schema.
Blockers: .str misuse.
Next: Generate holiday keywords.

Date: 2025-11-27

Learnt: Keyword engineering for NLP-style matching.
Built: generate_holiday_keywords.py.
Next: Holiday-to-menu matching.

Date: 2025-12-04

Learnt: Memory limits of Pandas at large scale.
Built: Initial matching script.
Blockers: OOM crashes.
Next: Chunk-based processing.

Date: 2025-12-14

Learnt: Streaming ETL patterns.
Built: Incremental CSV writing.
Next: Full pipeline run.

Date: 2025-12-15

Learnt: Running full-scale ETL pipelines.
Built: Generated ~76M holiday–menu matches.
Next: Analytics.

Date: 2025-12-16

Learnt: Scalable analytics on tens of millions of rows.
Built: Holiday popularity analytics pipeline.
Next: Dashboard metrics.

Date: 2025-12-17

Learnt: How FastAPI apps load in Uvicorn; Python imports.
Built: /health, /holidays/upcoming endpoints.
Blockers: ASGI app loading issues.
Next: Analytics endpoints.

Date: 2025-12-19

Learnt: Connecting React frontend to FastAPI backend.
Built: MVP dashboard showing upcoming holidays.
Next: Holiday of the Day card.

Date: 2025-12-21

Learnt: CORS, API contracts, MVP scoping.
Built: End-to-end CSV → API → UI flow.
Next: Shift focus from UI-first to insights-first.

Date: 2026-02-10

Learnt: How to design a real inference engine (baseline, momentum, confidence, action window).
Built:

Baseline Service

Momentum Service

Confidence Service

Action Window Service

/pulse/trends end-to-end inference pipeline
Blockers: Python env issues (resolved).
Next: Platform Bias Engine + crawler data contract.

🧠 Inference Engine v1 — COMPLETED (10 Feb 2026)

Baseline (abnormality vs norm)

Momentum (trend phase detection)

Confidence (risk-aware decision score)

Action Window (time-to-act + urgency)

Unified /pulse/trends endpoint with mock social pipeline

## ✅ Current Status (FoodLens Brain – v1) 11 Feb 2026

### What is built
- Unified /pulse/trends endpoint (mock + social source switch)
- Baseline deviation engine
- Momentum engine (velocity + acceleration + phase)
- Confidence engine (risk-aware, explainable)
- Action window estimation
- Platform Bias Engine (Uber Eats vs DoorDash vs Retail)
- Social ingestion pipeline (mock for TikTok, Instagram, YouTube)
- Social → Trend aggregation layer
- Social-derived time series adapter
- Multi-platform signal agreement (divergence-aware)
- Platform leader detection (TikTok / Instagram / YouTube / both)
- Debug endpoint: /pulse/debug to inspect raw social signals & platform momentum

### Key Product Philosophy
- UI is thin client
- Backend inference engine is the core product
- Directional accuracy > perfect prediction
- Explainability is first-class (confidence explanations, platform leader)

### Open Questions / Next Phase
- How to design scalable social data ingestion (scraping vs third-party tools)
- How to persist social signals into a database
- Whether to build full data engineering pipeline now vs MVP-first approach
- Schema design for social_signal, trend_signal, platform_signal tables
- Batch vs streaming ingestion (cron vs pub/sub)
- Cost-effective alternatives to official APIs (Instagram, TikTok)

## Current Status (FoodLens Brain – v1) — 15 Feb 2026

What is built
- /pulse/trends unified endpoint (mock + social)
- Baseline deviation engine
- Momentum engine (velocity, acceleration, phase)
- Confidence engine (risk-aware, explainable)
- Action window estimation
- Platform Bias Engine (Uber Eats, DoorDash, Retail)
- Social ingestion pipeline (pluggable dummy sources: TikTok, Instagram, YouTube)
- Social to Trend aggregation layer
- Social-derived time series adapter
- Multi-platform signal agreement
- Platform leader detection
- Debug endpoint: /pulse/debug

New Additions (21 Feb 2026)
- Raw social signals persisted in SQLite (system has memory)
- DB init script (init_db.py)
- Ingestion writes social data to DB
- Debug endpoint to view stored social data (/debug/social/raw)
- Time series now built from DB history (not just synthetic)
- Backdated ingestion simulation to create realistic trend spikes
- End-to-end pipeline validated: ingestion → DB → time series → momentum → confidence → platform bias
- Repo structure refactored: backend/ and frontend/ separation for cleaner architecture
- Frontend UI moved under frontend/ (prep for GitHub Pages / static hosting)

Product Philosophy
- UI is thin client
- Backend inference engine is the core product
- Directional accuracy over perfect prediction
- Explainability is first-class
- MVP-first data engineering (simulate before real crawlers/APIs)

Next Phase (Open Questions)
- Real social ingestion (scrapers, APIs, third-party tools)
- Schema evolution for raw_social_signals and trend tables
- Batch vs streaming ingestion
- Data freshness penalties in confidence engine
- Trend lifecycle modeling (emerging to peaking to fatigued)
- Deployment plan for TikTok ban workaround