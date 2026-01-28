✅ Setup Completed (till now) — UPDATED

Created GitHub repository for project.

Added README.md, LICENSE, and .gitignore.

Finalized project vision: Food Holiday Insight Engine (data → insights → dashboard → mobile app).

Agreed on project-first, learn-along-the-way approach.

Attempted web scraping (Playwright, Selenium, Requests).

Took an engineering decision to switch from unreliable scraping to static, authoritative food holiday dataset.

Built full data engineering pipeline handling millions of records.

📅 Learning & Project Timeline — REALIGNED STATUS
Phase 1: Data Collection (09/14/2025 – 09/27/2025)

 Learn Python basics for scraping (requests, BeautifulSoup, Selenium).

 Attempt real-world scraping (Playwright, Selenium).

 Evaluate scraping reliability & failures.

 Switch to static curated dataset for food holidays.

 Load Uber Eats menu dataset (millions of rows).

✅ Phase 1 effectively completed (with real-world tradeoff decision).

Phase 2: Data Storage (09/28/2025 – 10/11/2025)

 Use SQL (SQLite) for structured storage.

 Store Uber Eats menus in relational DB.

 Store food holidays in separate DB.

 Migrate to PostgreSQL (planned later).

 Optional NoSQL (MongoDB) later.

🟡 Phase 2 partially complete (SQLite now, Postgres later).

Phase 3: Data Processing (10/12/2025 – 10/25/2025)

 Pandas & NumPy for large-scale processing.

 Built ETL-style scripts.

 Implemented chunk-based processing.

 Generated ~76M holiday–menu matches.

 Analytics aggregation (Phase 2 analytics).

🟡 Phase 3 processing done, analytics starting now.

Phase 4: API Development (10/26/2025 – 11/08/2025)

 FastAPI / Flask backend.

 Serve analytics results via API.

⏳ Not started yet.

Phase 5: Frontend + Dashboard (11/09/2025 – 11/22/2025)

 Interactive dashboard (filters, KPIs).

 React-based web UI.

⏳ Not started yet.

Phase 6: AI/ML Integration (11/23/2025 – 12/06/2025)

 Popularity prediction.

 Recommendation engine.

⏳ Planned.

Phase 7: Deployment (12/07/2025 – 12/20/2025)

 Docker.

 Cloud deployment.

⏳ Planned.

🧾 Daily Log — POPULATED (Important Part)
Daily Progress Logs

 Date: 09/06/2025

What I learnt today: How to properly structure a GitHub project for a long-term data engineering project.

What I built/tested today: Created repo with README, LICENSE, .gitignore.

Blockers: None.

Next Steps: Start data sourcing via web scraping.

 Date: 09/13/2025

What I learnt today: Basics of Playwright scraping and how modern websites load data via APIs.

What I built/tested today: Ran Playwright scraper and captured JSON endpoints.

Blockers: Data not persisted; scraping complexity higher than expected.

Next Steps: Decide storage format and improve scraping reliability.

 Date: 09/24/2025

What I learnt today: Importance of documentation and planning for complex projects.

What I built/tested today: Drafted working_document.md and roadmap.

Blockers: None.

Next Steps: Finalize repo structure and data flow.

 Date: 10/15/2025

What I learnt today: Limitations of web scraping at scale (SSL issues, JS-heavy pages, blocking).

What I built/tested today: Multiple scraping attempts using Requests, Selenium, BeautifulSoup.

Blockers: Scrapers returned incomplete or zero data.

Next Steps: Explore alternative data sources.

 Date: 11/06/2025

What I learnt today: When to replace scraping with curated datasets in real projects.

What I built/tested today: Loaded static food holidays CSV; built load_holidays_static.py.

Blockers: Encoding issues, column mismatches.

Next Steps: Clean and normalize holiday dataset.

 Date: 11/20/2025

What I learnt today: Handling CSV encoding issues and Pandas data cleaning pitfalls.

What I built/tested today: Fixed loader script; validated holiday table schema.

Blockers: Pandas .str misuse on DataFrame.

Next Steps: Generate holiday keywords.

 Date: 11/27/2025

What I learnt today: Keyword engineering for NLP-style matching.

What I built/tested today: Created generate_holiday_keywords.py.

Blockers: None.

Next Steps: Match holidays to menu items.

 Date: 12/04/2025

What I learnt today: Memory limits of Pandas at tens of millions of rows.

What I built/tested today: Initial holiday-to-menu matching script.

Blockers: Out-of-memory crashes.

Next Steps: Refactor to chunk-based processing.

 Date: 12/14/2025

What I learnt today: Streaming ETL patterns and incremental file writes.

What I built/tested today: Refactored matching pipeline to write CSV incrementally.

Blockers: Performance tuning.

Next Steps: Complete full run and validate output.

 Date: 12/15/2025

What I learnt today: End-to-end data pipeline execution at scale.

What I built/tested today: Successfully generated ~76M holiday–menu matches.

Blockers: None (long runtime expected).

Next Steps: Start analytics (Phase 2).

 Date: 12/16/2025

* What I learnt today:
- How to compute scalable analytics on tens of millions of rows using chunked processing
- How real-world “popularity scores” are derived for product dashboards

* What I built/tested today:
- Holiday popularity analytics pipeline
- Generated `holiday_popularity.csv` with normalized 0–100 popularity scores
- Started computing top dishes per holiday (long-running job)

* Blockers:
- Long execution time due to large dataset (expected, not an issue)

* Next Steps:
- Complete top dishes per holiday analytics
- Use results for dashboard metrics
(keep remaining dates as-is)

Date: 12/17/2025

* What I learnt today:
    Learned how FastAPI apps are discovered by Uvicorn, how Python module imports work in real projects, and how to debug ASGI app loading issues.

* What I built/tested today:
Successfully created and ran the first FastAPI service (`src/api/main.py`) with live endpoints:
`/`, `/health`, and `/holidays/upcoming`.

* Blockers:
API initially failed due to missing `app` object being exported from the module.

* Next Steps:
Expose analytics-driven endpoints (holiday popularity, top dishes per holiday) and connect them to the API.

Date: 12/18/2025

  * What I learnt today:
    Learned how FastAPI apps are discovered by Uvicorn, how Python module imports work in real projects, and how to debug ASGI app loading issues.

  * What I built/tested today:
    Successfully created and ran the first FastAPI service (`src/api/main.py`) with live endpoints:
    `/`, `/health`, and `/holidays/upcoming`.

  * Blockers:
    API initially failed due to missing `app` object being exported from the module.

  * Next Steps:
    Expose analytics-driven endpoints (holiday popularity, top dishes per holiday) and connect them to the API.

Date: 12/19/2025s

- What I learnt today:
  How to connect a React frontend to a FastAPI backend using fetch.

- What I built/tested today:
  Successfully displayed real upcoming food holidays in the MVP dashboard.

- Blockers:
  None.

- Next Steps:
  Connect “Holiday of the Day” and trending analytics.

- Date: 12/20/2025
  - Fixed FastAPI startup error caused by missing app initialization.
  - Properly defined FastAPI app instance.
  - Backend endpoint now starts successfully.

Date: 12/21/2025

  * What I learnt today:
    - How to connect a FastAPI backend with a React (Vite) frontend.
    - How CORS issues arise when frontend and backend run on different ports.
    - How API contracts (JSON shape) directly affect frontend rendering.
    - How an MVP should be minimal and focused, not over-engineered.

  * What I built/tested today:
    - Successfully exposed `/holidays/upcoming` API from FastAPI.
    - Verified backend reads from `food_holidays_static.csv`.
    - Built a React frontend that fetches upcoming holidays.
    - Rendered upcoming holidays dynamically in the UI.
    - Fixed multiple backend errors (missing imports, incorrect paths, table assumptions).
    - Confirmed end-to-end data flow: CSV → API → UI.

  * Blockers:
    - Initial CORS errors between frontend (5173) and backend (8000).
    - Path/import errors in FastAPI (`Path`, `app` not defined).
    - Confusion due to backend being run from the wrong directory at times.

  * Next Steps:
    - Add “Dish of the Day” card (Step 3 – Part 1).
    - Keep it static first (mock data) to finalize UI layout.


🎯 Where you are NOW (very clearly)

✅ Foundation — done

✅ Data engineering — done

🟡 Phase 2 Analytics — STARTING NOW

⏳ Dashboard / Web / Mobile — coming next