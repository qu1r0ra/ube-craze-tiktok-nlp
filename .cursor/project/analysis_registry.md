# Analysis Registry

This registry tracks the findings, sentiment models, and plot outputs generated during the analysis.

## Sentiment Analysis Models

- **Primary Model**: `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Output Labels**: `negative`, `neutral`, `positive`

## Visualization Figures

Generated plots will be exported to `outputs/` and recorded here.

| Figure Filename                | Description                                                    | Output Path | Status  |
| :----------------------------- | :------------------------------------------------------------- | :---------- | :------ |
| `sentiment_distribution.png`   | Overall distribution of sentiment across all comments          | `outputs/`  | Pending |
| `word_frequency_pride.png`     | High-frequency keywords from positive (pride) comments         | `outputs/`  | Pending |
| `word_frequency_exotic.png`    | High-frequency keywords from negative/neutral comments         | `outputs/`  | Pending |
| `word_frequency_bigrams.png`   | Top bigram phrases from positive vs negative/neutral comments  | `outputs/`  | Pending |
| `word_frequency_trigrams.png`  | Top trigram phrases from positive vs negative/neutral comments | `outputs/`  | Pending |
| `topic_clusters_sentiment.png` | Sentiment breakdown across unsupervised K-Means topic clusters | `outputs/`  | Pending |
| `reply_sentiment_heatmap.png`  | Parent-reply comment sentiment transition heatmap              | `outputs/`  | Pending |
