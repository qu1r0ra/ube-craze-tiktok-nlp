# Ube Craze NLP Workspace Handoff

Living document for agent-to-agent and session-to-session continuity for the GEWORLD (The Contemporary World) Ube Craze TikTok NLP project.

| Field                  | Value                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Last updated**       | 2026-06-30                                                                                                                                                   |
| **Last session focus** | Reorganized outputs/ into plots/, clusters/, and docs/, added new visualizations, resolved mathematical artifacts using LSA SVD, and tracked outputs in Git. |
| **Active repo**        | `ube-craze-tiktok-nlp`                                                                                                                                       |
| **Blockers**           | None (pipeline runs completed successfully)                                                                                                                  |

---

## 1. Quick Start (New Agent)

1. Open this workspace in VS Code / Cursor.
2. Read the approved proposal in [docs/proposal.md](docs/proposal.md).
3. Read this file end-to-end, then review the implementation queue in [Section 5](#5-implementation-queue).
4. Run `uv sync` to ensure your virtual environment is synchronized.
5. Populate `links.txt` at the root with 67 target TikTok video URLs (done by developer).
6. Run `uv run python -m ube_craze_nlp.scraper.engine` to scrape metadata and comment payloads.
7. Run preprocessing, sentiment analysis, and visualization notebooks in the `notebooks/` directory. (On Windows, prefix command execution with `$env:PYTHONIOENCODING="utf-8";` to prevent encoding crashes on emojis).
8. Before ending a session, update this file and update `AGENTS.md` to record status.

---

## 2. Workspace Map

| Resource / Path                          | Role                | Description                                                                                                       |
| :--------------------------------------- | :------------------ | :---------------------------------------------------------------------------------------------------------------- |
| [docs/proposal.md](docs/proposal.md)     | Approved Proposal   | Research proposal on digital gastronationalism & Ube trend.                                                       |
| [src/ube_craze_nlp/](src/ube_craze_nlp/) | Main Python Package | Source code directory containing the scraper, NLP pipeline, and utilities.                                        |
| [notebooks/](notebooks/)                 | Jupyter Notebooks   | Interactive notebooks for Scraping (01), Preprocessing (02), Sentiment (03), and Viz (04).                        |
| [data/](data/)                           | Data Pipeline       | Ignored folder hosting raw scrapes (`raw/`), filtered text (`processed/`), and final analysis outputs (`final/`). |
| [outputs/](outputs/)                     | Plots & Visuals     | Ignored folder for generated figures, plots, and charts.                                                          |
| [.cursor/rules/](.cursor/rules/)         | Domain Rules        | Custom agentic rules for the workspace (`tech-stack.mdc`, `project-overview.mdc`).                                |
| [.cursor/project/](.cursor/project/)     | Project Registries  | Registries tracking data files (`data_registry.md`) and analysis logs (`analysis_registry.md`).                   |

---

## 3. Locked Architectural Decisions

| Topic               | Decision                             | Details                                                                                                                                                                         |
| :------------------ | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Data Source**     | TikTok only                          | Constrained to TikTok comments and metadata based on Scope and Limitations (6-week timeline).                                                                                   |
| **Scraper Style**   | Playwright + Network Interception    | Intercepts JSON responses from TikTok's API endpoints. Automatically triggers the Comments tab and scrolls using updated `CommentMain` selectors to bypass 'You may like' tabs. |
| **Scraper Inputs**  | `links.txt` file                     | List of exactly 67 high-engagement video URLs to ensure human relevance and bypass search walls.                                                                                |
| **NLP Language**    | English, Tagalog, and Taglish        | Filtered using `lingua-language-detector` to discard other languages.                                                                                                           |
| **Sentiment Model** | `twitter-xlm-roberta-base-sentiment` | Multilingual transformer executed locally offline for robust mixed-language (Taglish) sentiment.                                                                                |
| **Packaging**       | `uv` with Hatchling backend          | Replicates professional standard; package root resolved dynamically. Includes `requests` package.                                                                               |

---

## 4. Current Status

### Phase 1: Scaffolding [Complete]

- Directories created: `references/`, `data/`, `notebooks/`, `outputs/`, `src/ube_craze_nlp/`, `tests/`.
- Dependency management configured via `pyproject.toml` using `uv`.
- Playwright Chromium browser installed.
- Agentic rules (`tech-stack.mdc`) and indices (`AGENTS.md`) created.

### Phase 2: TikTok Scraper [Complete]

- Playwright network interception engine (`engine.py`) and response parser (`parser.py`) fully implemented, upgraded to handle new desktop tab layouts and updated class selectors, and successfully unit-tested.

### Phase 3: NLP & Preprocessing [Complete]

- Language filtering (Lingua) and text normalization/stopword removal (`clean.py`) fully implemented and tested.
- Local multilingual XLM-RoBERTa sentiment analysis pipeline (`sentiment.py`) fully implemented and tested.

### Phase 4: Jupyter Notebooks & Visualizations [Complete]

- Notebooks `01` through `04` fully generated, documented, and updated with advanced NLP sections (Bigrams, Trigrams, K-Means clustering, and Sentiment transition heatmap). All visualizations verified.

### Phase 5: Bulk Execution & Data Generation [Complete]

- Headless browser configuration tested and verified; executed scraper successfully in the background to harvest all 67 video targets, yielding 9,504 raw comments.
- Fixed CardiffNLP label mapping bug in `sentiment.py` to prevent incorrect neutral defaulting.
- Created `scripts/run_pipeline.py` runner to execute the preprocessing, sentiment scoring, and plotting notebooks automatically and non-blockingly using Matplotlib's `'Agg'` backend.
- Separated neutral and negative comment subsets in the word/N-gram frequency analyses to avoid drowning active friction/resistance under neutral botanical/product descriptions.
- Generated and saved `cleaned_comments.csv` (6,137 unique comments) and `sentiment_scored_comments.csv`, and reorganized all 20+ visualization/analysis outputs into `outputs/` subfolders (plots, clusters, and docs). This includes general frequency/sentiment plots (`outputs/plots/`), elbow curve, cluster size distribution, stacked sentiment breakdown, stacked language distribution, individual word clouds, and grid layouts (`outputs/clusters/`), and qualitative documents (`outputs/docs/cluster_insights.md` and `outputs/docs/cluster_samples.md`).

---

## 5. Implementation Queue

|  P  | Task                                                                                        | Component | Status |
| :-: | :------------------------------------------------------------------------------------------ | :-------- | :----- |
|  1  | Create scraper engine (`engine.py`) and response parser (`parser.py`)                       | Scraper   | [x]    |
|  2  | Setup `links.txt` template and run test scrape                                              | Scraper   | [x]    |
|  3  | Implement language filtering & text normalization (`nlp/clean.py`)                          | NLP       | [x]    |
|  4  | Implement local XLM-RoBERTa sentiment model (`nlp/sentiment.py`)                            | NLP       | [x]    |
|  5  | Write pytest test suites for scraper & text processors                                      | Tests     | [x]    |
|  6  | Create Jupyter Notebooks 01 through 04                                                      | Notebooks | [x]    |
|  7  | Generate sentiment visualization plots and export                                           | Outputs   | [x]    |
|  8  | Add 67 target video URLs to `links.txt` and execute pipeline                                | Execution | [x]    |
|  9  | Implement bigram/trigram, unsupervised clustering, and reply sentiment interaction analysis | Analysis  | [x]    |

---

## 6. Environment and Secrets

- Create a `.env` file at the root if environment variables (e.g. proxy credentials, logging levels) are added.
- **`links.txt`**: Created at the root directory; populate with 67 TikTok video URLs.

---

## 7. Agent Conventions

- **Registries**: Always update [.cursor/project/data_registry.md](.cursor/project/data_registry.md) when data files are scraped or processed.
- **Ruff**: Before finalizing code changes, run `uv run ruff check` and `uv run ruff format` to ensure style correctness.
- **No Emojis**: Do not use emojis in codebase files (Python, configs) other than documentation headers if justified.

---

## 8. Next Steps (Future Analysis)

1. **Qualitative Synthesis:** [Complete] Implemented pipeline refinements (LSA/TruncatedSVD + custom stopwords) to generate highly coherent clusters, resolving the sticker-dominated and tiny 8-comment artifacts. Reorganized `outputs/` into subdirectories and updated descriptions in [cluster_insights.md](outputs/docs/cluster_insights.md) and [cluster_samples.md](outputs/docs/cluster_samples.md).
2. **Interaction Matrix Interpretation:** Analyze the [reply_sentiment_heatmap.png](outputs/plots/reply_sentiment_heatmap.png) to determine how the community responds to negative/exoticizing parents vs. positive ones (soft power dynamics).
3. **Drafting Findings:** Synthesize the sentiment transitions and topic frequencies into the final GEWORLD gastronationalism research paper and documentary script.
