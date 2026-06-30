# Data Registry

This registry tracks the datasets generated during the scraping and preprocessing phases.

| File / Directory Path | Phase         | Format            | Records | Status / Notes                                                               |
| :-------------------- | :------------ | :---------------- | :------ | :--------------------------------------------------------------------------- |
| `data/raw/`           | Scraping      | Folder (JSON/MP4) | -       | Awaiting execution. Will contain individual directories per video ID.        |
| `data/processed/`     | Preprocessing | Folder (CSV)      | -       | Awaiting execution. Will hold language-filtered, tokenized comment datasets. |
| `data/final/`         | Analysis      | Folder (CSV)      | -       | Awaiting execution. Final sentiment-scored comment datasets.                 |

## Scraped Videos Log

This section will list the 30 scraped TikTok video IDs, authors, titles, and comment counts once Phase 2 runs.

| Video ID | Author | Description / Topic               | Total Comments Scraped | Scraped Date |
| :------- | :----- | :-------------------------------- | :--------------------- | :----------- |
|          |        | _(To be populated post-scraping)_ |                        |              |
