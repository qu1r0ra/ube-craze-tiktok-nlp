# Data Registry

This registry tracks the datasets generated during the scraping and preprocessing phases.

| File / Directory Path | Phase         | Format            | Records | Status / Notes                                                               |
| :-------------------- | :------------ | :---------------- | :------ | :--------------------------------------------------------------------------- |
| `data/raw/`           | Scraping      | Folder (JSON/MP4) | -       | Awaiting execution. Will contain individual directories per video ID.        |
| `data/processed/`     | Preprocessing | Folder (CSV)      | -       | Awaiting execution. Will hold language-filtered, tokenized comment datasets. |
| `data/final/`         | Analysis      | Folder (CSV)      | -       | Awaiting execution. Final sentiment-scored comment datasets.                 |

## Scraped Videos Log

This section will list the 67 scraped TikTok video IDs, authors, titles, and comment counts once Phase 2 runs.

| Video ID | Author | Description / Topic               | Total Comments Scraped | Scraped Date |
| :------- | :----- | :-------------------------------- | :--------------------- | :----------- |
|          |        | _(To be populated post-scraping)_ |                        |              |

## Search Methodology & Sampling Strategy

The dataset is selected using a **Keyword-Based Purposive Sampling** strategy targeting TikTok videos published between 2024 and 2026. A total of **67 videos** were curated for scraping.

### Sampling Criteria

1. **Search Keywords**: Videos were searched using the following query terms:
   - `ube`
   - `ube craze`
   - `trader joes ube`
   - `foreigner tries ube`
   - `purple yam`
   - `ube pronunciation`
2. **Engagement & Discussion Quality (Manual Verification)**:
   - **Like Verification**: Prioritized videos with relatively high like counts within each search query to ensure high reach and visibility.
   - **Discussion Scanning**: Scanned comment feeds to verify that the video generated active, meaningful, and relevant dialogue (such as discussions of cultural authenticity, heritage representation, or consumption behavior) rather than generic spam.
3. **Excluded Keywords**: Keywords like `filipino ube` and `ube taste test` were removed from active query lists as they did not yield distinct or significant additional search results.
