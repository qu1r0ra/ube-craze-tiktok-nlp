# Analysis Registry

This registry tracks the findings, sentiment models, and plot outputs generated during the analysis.

## Sentiment Analysis Models

- **Primary Model**: `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Output Labels**: `negative`, `neutral`, `positive`

## Visualization Figures

Generated plots will be exported to `outputs/` and recorded here.

| Figure Filename              | Description                                            | Output Path | Status  |
| :--------------------------- | :----------------------------------------------------- | :---------- | :------ |
| `sentiment_distribution.png` | Overall distribution of sentiment across all comments  | `outputs/`  | Pending |
| `word_frequency_pride.png`   | High-frequency keywords from positive (pride) comments | `outputs/`  | Pending |
| `word_frequency_exotic.png`  | High-frequency keywords from negative/neutral comments | `outputs/`  | Pending |
