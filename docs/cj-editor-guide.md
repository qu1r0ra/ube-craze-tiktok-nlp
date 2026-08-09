# CJ Research Findings — Editor’s Guide

This guide supports the **Research Findings: (CJ)** section in [video-script.md](video-script.md). The section should feel like a concise documentary analysis: begin with the overall comment landscape, move through concrete examples of cultural boundary-policing, then end by connecting cultural recognition to material concerns.

## Editorial objective

The audience should leave with this idea:

> Global appreciation for ube is real, but meaningful appreciation requires cultural accuracy, recognition, and responsibility.

Do not frame the findings as “Filipinos dislike foreigners enjoying ube.” The evidence shows a more complicated pattern: people welcome interest in ube while challenging mispronunciation, ingredient substitution, cultural erasure, and unequal economic benefits.

## Target duration and pacing

- **Target duration:** 2:40–3:00, including pauses and visual transitions.
- **Core narration:** approximately 400 spoken words.
- **Editing style:** calm documentary pacing; use short comment flashes and gentle chart transitions rather than rapid meme editing.
- **If the section is too long:** cut the optional agricultural statistic sentence first, then shorten the positive-appreciation paragraph. Keep the pronunciation, culinary-boundary, and synthesis beats.

## Recommended edit map

| Approx. time | Spoken beat | Visual treatment | Editor’s purpose |
|---|---|---|---|
| 0:00–0:10 | “What did people actually say?” | TikTok comment montage; purple accent title | Bridge from Claire’s discussion of social media into the project’s evidence | 
| 0:10–0:30 | Dataset and sentiment overview | Show `outputs/plots/sentiment_distribution.png`; animate the three percentages one at a time | Establish that the discussion is mixed, not simply celebratory | 
| 0:30–0:48 | Positive appreciation | Show one welcoming comment, then a brief montage of ube desserts and Filipino cooking | Preserve the positive side of the findings | 
| 0:48–1:18 | Pronunciation as respect | Show pronunciation comments and then pronunciation-related word clouds | Make the first form of digital boundary-policing concrete | 
| 1:18–1:52 | Ube versus taro/purple sweet potato | Split-screen labels: `UBE` / `TARO` / `PURPLE SWEET POTATO`; show a short correction comment | Explain that authenticity concerns involve ingredients, not only names | 
| 1:52–2:25 | Matcha-fication and material concerns | Show `outputs/clusters/cluster_sentiment_stacked.png` or `outputs/clusters/topic_clusters_wordclouds_sentiment.png`; overlay keywords `farmers`, `prices`, `shortages`, `matcha` | Connect cultural recognition to agriculture and economic consequences | 
| 2:25–2:50 | Synthesis and handoff | Collage of appreciative and critical comments; hold on a final “recognition + responsibility” card | Prepare Shin’s conclusion and call to action | 

The exact timings may shift with delivery speed. The sequence matters more than the timestamps.

## Specific comments to use

Use short excerpts that are readable on screen. Keep each comment visible for roughly 2–3 seconds, or longer if it is being discussed. Crop or blur usernames unless the group has permission to display them.

### 1. Positive appreciation

Recommended comment:

> “i love seeing people enjoy mu cultrure’s food 🥰🥰🥰”

Use this immediately after the sentiment chart. It prevents the segment from presenting every reaction as hostile and supports the point that international interest can be genuine.

Optional alternative:

> “We promise we didn’t invent Ube 😭💜 Just making sure she gets the spotlight she deserves!”

If emojis are displayed, preserve them in the screenshot but do not add emojis to the narration or charts.

### 2. Pronunciation as respect

Recommended sequence:

> “it’s pronounced U-BE”

Then show a second correction:

> “It’s pronounced oo-beh. I hope it can be pronounced properly. But thank you for saying it’s from the Philippines!”

The second comment is especially useful because it shows correction and appreciation coexisting in the same response. The visual should emphasize the pronunciation correction, not mock the person who mispronounced the word.

### 3. Culinary boundaries

Recommended comment:

> “Taro and ube are different things?!?”

Follow with a more explanatory comment if space allows:

> “Ube is described to be almost vanilla-like in taste while taro is light and nutty.”

For the visual, use a simple three-column comparison rather than a dense botanical chart. The narration’s point is that commenters were defending a culinary identity, not proving that one root crop is morally superior to another.

### 4. Agricultural and economic concerns

Recommended comment:

> “The Government should invest more in our agriculture😭”

Optional supporting comment:

> “im gonna fcking cry if ube gets more expensive”

Use these only after the audience has seen the cluster or keyword visual. They make the transition from online cultural debate to farmers, prices, and supply concerns understandable.

### 5. Matcha-fication anxiety

Recommended comment:

> “it’s becoming like matcha”

Optional alternative:

> “we might have a shortage of ube if it truly gets popular similar to matcha”

The narration should attribute this interpretation to commenters. Use wording such as **“commenters compared ube’s future to matcha’s”**, not **“ube is being gentrified”** as an unqualified fact.

## Visualization instructions

### Sentiment distribution

File: [outputs/plots/sentiment_distribution.png](../outputs/plots/sentiment_distribution.png)

Show the chart during the sentence containing the three percentages:

- **35.8% neutral**
- **33.8% negative**
- **30.4% positive**

Recommended treatment:

1. Begin with the full chart for orientation.
2. Highlight each segment as CJ names it.
3. Add a small caption: **“6,137 analyzed comments”**.
4. Add a footnote or end-card note: **“Sentiment labels are model classifications, not a survey of all Filipinos.”**

Do not imply that the negative percentage means 33.8% of Filipinos oppose ube globalization. It describes this analyzed comment dataset.

### Topic clusters

Primary file: [outputs/clusters/topic_clusters_wordclouds_sentiment.png](../outputs/clusters/topic_clusters_wordclouds_sentiment.png)

Alternative file: [outputs/clusters/cluster_sentiment_stacked.png](../outputs/clusters/cluster_sentiment_stacked.png)

The narration discusses three anchor findings, but the project identified seven clusters. Show the seven-cluster grid briefly, then zoom or cut to the relevant themes:

- Pronunciation correction
- Mainstream discussion and economy
- Appreciation and labor
- “Oob” backlash and memes
- Matcha-fication and gentrification anxiety
- Ube versus taro culinary boundaries
- Botanical and technical accuracy

Do not leave the full seven-cluster grid on screen long enough for viewers to read every label. Use it as a map, then use larger text for the three spoken anchors.

### Cluster sentiment chart

File: [outputs/clusters/cluster_sentiment_stacked.png](../outputs/clusters/cluster_sentiment_stacked.png)

Use this as a transition into the material-concerns paragraph. Avoid narrating every bar. Instead, highlight the cluster associated with mainstream discussion and economy, then overlay the words **“farmers,” “prices,” and “supply.”**

The script currently states that this largest cluster contains **82.7% of comments**. Keep the phrase **“in our dataset”** nearby so the statistic is not mistaken for a population estimate.

### Optional supporting visuals

- [outputs/plots/word_frequency_bigrams.png](../outputs/plots/word_frequency_bigrams.png): use for a 1–2 second transition if the editor wants additional evidence for phrases such as `ube halaya`, `purple yam`, `taro taste`, and `matcha latte`.
- [outputs/plots/reply_sentiment_heatmap.png](../outputs/plots/reply_sentiment_heatmap.png): optional only. It is useful if the editor wants to show that replies can intensify or reinforce the parent comment’s tone, but it is not necessary for CJ’s core argument.
- [outputs/docs/cluster_insights.md](../outputs/docs/cluster_insights.md): reference document for checking cluster labels and interpretations.
- [outputs/docs/cluster_samples.md](../outputs/docs/cluster_samples.md): source document for locating additional comment examples.

## On-screen text recommendations

Keep overlays short enough to read while listening:

- `6,137 analyzed comments`
- `35.8% neutral · 33.8% negative · 30.4% positive`
- `Pronunciation became a test of respect`
- `UBE ≠ TARO ≠ PURPLE SWEET POTATO`
- `Cultural recognition has material consequences`
- `Appreciation → Recognition → Responsibility`

Avoid placing full paragraphs, methodology details, or all cluster keywords over the speaker. Those belong in the narration, chart labels, or supporting documentation.

## Accuracy and tone safeguards

- Say **“comments in our dataset”** or **“many commenters”**, not **“Filipinos believe”** or **“Filipinos reject.”**
- Say **“the model classified comments as…”** when describing sentiment percentages.
- Say **“commenters described this as…”** when using terms such as gentrification, appropriation, or cultural erasure.
- Do not treat pronunciation correction as proof that every pronunciation variant is equally unacceptable; frame it as a recurring form of cultural gatekeeping in the comment discourse.
- Do not equate taro with a bad ingredient. The finding concerns substitution or mislabeling when taro is presented as authentic ube.
- Preserve the positive comments so the section reflects both cultural pride and cultural anxiety.
- Blur usernames, profile photos, and identifying information unless permission has been obtained.

## Minimum viable version if editing time is limited

If the editor needs a compact version, retain only:

1. The sentiment distribution chart and the three percentages.
2. One positive appreciation comment.
3. The “it’s pronounced U-BE” comment.
4. The ube-versus-taro comparison card.
5. One farmer or price concern comment.
6. The final collage and handoff line.

This preserves the complete argument: appreciation is present, but recognition and responsibility shape how that appreciation is received.
