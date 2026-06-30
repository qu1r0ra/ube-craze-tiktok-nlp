# Analysis Registry

This registry tracks the findings, sentiment models, and plot outputs generated during the analysis.

## Sentiment Analysis Models

- **Primary Model**: `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Output Labels**: `negative`, `neutral`, `positive`

## Visualization Figures

Generated plots and qualitative reports are organized into specific subdirectories under `outputs/`.

### General Plots (`outputs/plots/`)

| Figure Filename                                                                | Description                                                       | Status    |
| :----------------------------------------------------------------------------- | :---------------------------------------------------------------- | :-------- |
| [sentiment_distribution.png](../../outputs/plots/sentiment_distribution.png)   | Overall distribution of sentiment across all comments             | Generated |
| [word_frequency_pride.png](../../outputs/plots/word_frequency_pride.png)       | High-frequency keywords from positive (pride) comments            | Generated |
| [word_frequency_neutral.png](../../outputs/plots/word_frequency_neutral.png)   | High-frequency keywords from neutral (context) comments           | Generated |
| [word_frequency_exotic.png](../../outputs/plots/word_frequency_exotic.png)     | High-frequency keywords from negative (friction) comments         | Generated |
| [word_frequency_bigrams.png](../../outputs/plots/word_frequency_bigrams.png)   | Top bigram phrases from positive, neutral, and negative comments  | Generated |
| [word_frequency_trigrams.png](../../outputs/plots/word_frequency_trigrams.png) | Top trigram phrases from positive, neutral, and negative comments | Generated |
| [reply_sentiment_heatmap.png](../../outputs/plots/reply_sentiment_heatmap.png) | Parent-reply comment sentiment transition heatmap                 | Generated |

### Clustering Analytics (`outputs/clusters/`)

| Figure Filename                                                                                           | Description                                                     | Status    |
| :-------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- | :-------- |
| [kmeans_elbow_curve.png](../../outputs/clusters/kmeans_elbow_curve.png)                                   | K-Means Elbow curve (inertia analysis for K=2..12)              | Generated |
| [cluster_size_distribution.png](../../outputs/clusters/cluster_size_distribution.png)                     | sorted distribution of comment counts per cluster               | Generated |
| [cluster_sentiment_stacked.png](../../outputs/clusters/cluster_sentiment_stacked.png)                     | Stacked bar chart showing sentiment breakdown (%) per cluster   | Generated |
| [cluster_language_stacked.png](../../outputs/clusters/cluster_language_stacked.png)                       | Stacked bar chart showing language distribution (%) per cluster | Generated |
| [topic_clusters_wordclouds_sentiment.png](../../outputs/clusters/topic_clusters_wordclouds_sentiment.png) | Combined Word Clouds and sentiment distributions (grid format)  | Generated |
| `cluster_[0-6]_wordcloud.png`                                                                             | Individual high-resolution word clouds for each topic cluster   | Generated |

### Qualitative Analysis Reports (`outputs/docs/`)

| Document Filename                                             | Description                                                       | Status    |
| :------------------------------------------------------------ | :---------------------------------------------------------------- | :-------- |
| [cluster_samples.md](../../outputs/docs/cluster_samples.md)   | Representative sample comments (25 liked + 25 random) per cluster | Generated |
| [cluster_insights.md](../../outputs/docs/cluster_insights.md) | Refined thematic mappings and takeaways for the K=7 clusters      | Refined   |
