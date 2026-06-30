# K-Means Topic Clustering Refined Insights (K=7, TF-IDF + LSA)

This document records the qualitative analysis, themes, and sociopolitical/gastronationalist implications of the 7 topic clusters generated using our refined preprocessing (visual/grammatical noise filtered) and dimensionality reduction (TruncatedSVD/LSA) pipeline.

---

## Thematic Mapping of Clusters

| Cluster       | Key Terms                                     | Core Theme                             | Sociopolitical / Gastronationalist Implication                                                                                                                                                                               |
| :------------ | :-------------------------------------------- | :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cluster 0** | `pronounced`, `oob`, `oobay`, `oobeh`         | Pronunciation Correction & Orthography | Highlights how correct pronunciation is used as a gatekeeping metric for cultural respect. Commenters actively correct foreigners to preserve linguistic authenticity.                                                       |
| **Cluster 1** | `taste`, `halaya`, `real`, `omg`, `flavor`    | Mainstream & Socioeconomic Catch-All   | Serves as the primary discussion hub (82.7% of comments). It is the center of domestic agricultural critique (e.g. government neglect of farmers, rising prices, and supply chain failures) alongside colonization concerns. |
| **Cluster 2** | `love`, `oob`, `labor`, `halaya`, `delicious` | Cultural Appreciation & Empathy        | Focuses on positive global engagement, where foreigners express love for the flavor and Filipinos appreciate their culture being shared (with warnings on labor-intensiveness).                                              |
| **Cluster 3** | `oob`, `called`, `wtf`, `bro`, `calling`      | Emotive "Oob" Backlash & Memes         | Captures the raw community reaction and shock to viral mispronunciations (e.g., "oob"). Represents a defensive, meme-driven response to cultural distortion.                                                                 |
| **Cluster 4** | `matcha`, `purple`, `japan`, `latte`          | "Matcha-fication" & Gentrification     | Discusses the fear that ube will follow matcha's path—being stripped of cultural credit, gentrified by global chains, and suffering raw material shortages/price spikes.                                                     |
| **Cluster 5** | `taro`, `taste`, `gabi`, `love`, `sinigang`   | Taro vs. Ube Culinary Boundary         | Fights against the commercial practice of substituting ube with cheaper taro powder and food coloring. Commenters clarify the flavor differences to protect ube's unique culinary identity.                                  |
| **Cluster 6** | `purple`, `yam`, `potato`, `sweet`, `taro`    | Botanical & Technical Classification   | Educational discourse clarifying that ube is a purple yam (`dioscorea alata`), not a sweet potato or taro. Represents efforts to establish botanical accuracy globally.                                                      |

---

## Key Analytical Takeaways

### 1. The Socioeconomic Anchor of Digital Pride (Cluster 1)

- Rather than digital gastronationalism being purely about cultural symbols, it is deeply anchored in material realities. Local Filipinos use the global popularity of ube to criticize domestic agricultural policy—specifically calling out the Department of Agriculture, land-grabbing, and the exploitation of local farmers by middlemen, while warning of local shortages.

### 2. Pronunciation as a Battleground for Respect (Clusters 0 & 3)

- Correcting the viral mispronunciation "oob" is the most common form of everyday digital resistance. Commenters view pronunciation not just as accents, but as a test of whether global consumers respect the culture they are consuming.

### 3. The Matcha Precedent and Gentrification Anxiety (Cluster 4)

- The community uses matcha as a cautionary tale. They fear corporate "matcha-fication," where ube becomes a gentrified, generic purple aesthetic flavor sold at a premium by global brands (like Starbucks) without cultural recognition or benefit to the Philippines.

### 4. Culinary Integrity and Taro Substitution (Cluster 5)

- Commenters express active resistance to mainstream Western cafes using cheap taro powder/extract and purple dye under the name of "ube." They assert that authentic ube has a distinct vanilla-like profile that cannot be substituted, protecting the culinary standard of their heritage.

---

## Methodological Selection of K=7 (Validation Sweep)

To determine the optimal cluster size, we performed a qualitative validation sweep across adjacent values ($K \in [5, 8]$) to evaluate thematic coherence and overlap:

### 1. Diagnostic Summary of Adjacent Runs

- **K = 5 (Under-Clustering)**:
  - **Theme Merging**: Matcha-fication (gentrification) and Taro substitution (flavor boundaries) were collapsed into a single catch-all cluster (`matcha, taro, halaya, omg, flavor, real`).
  - **Implication**: We lose the analytical granularity to distinguish between corporate macroeconomic anxieties (Starbucks gentrification) and culinary/botanical integrity (resisting taro substitution).
- **K = 6 (Under-Clustering)**:
  - **Theme Merging**: Still failed to isolate matcha and taro. The domestic agricultural policy critique (`government`) was compressed alongside general culinary comments into Cluster 0.
- **K = 7 (Optimal Inflection Point)**:
  - **Granularity**: Cleanly isolates all key theoretical variables: orthographic pronunciation correction (Cluster 0), emotive backlash/memetic defense (Cluster 3), corporate matcha-fication (Cluster 4), taro flavor boundary enforcement (Cluster 5), and botanical accuracy (Cluster 6).
  - **Implication**: Maximizes interpretability and aligns perfectly with critical media studies frameworks.
- **K = 8 (Over-Clustering & Redundancy)**:
  - **Topic Redundancy**: Split botanical/visual classifications into two redundant clusters: Cluster 3 (`sweet, potato, purple, yam...`) and Cluster 5 (`purple, yam, color, yum...`).
  - **Topic Collapse**: Re-collapsed pronunciation correction and emotive memes back into a single Cluster 1 (`oob, pronounced, called...`), losing the nuance of different forms of cultural gatekeeping.

### 2. Validation Verdict

Selecting **$K=7$** provides the most theoretically coherent and semantically distinct division of comments, providing a strong empirical base for mixed-methods and qualitative gastronationalist analysis.
