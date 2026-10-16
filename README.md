# Ube discourse NLP: course showcase

An archived GEWORLD (The Contemporary World) course project exploring TikTok discussions about ube through language filtering, multilingual sentiment classification, and TF-IDF/LSA clustering. Publication revival is not planned.

## What remains useful

`src/ube_craze_nlp/` contains the original parser, preprocessing, sentiment wrapper, and local video utilities. `notebooks/` preserves the coursework pipeline with cleared outputs. Parser tests use invented fixtures. A small public demonstration is available without collecting data or downloading models:

```bash
python scripts/build_editor_guide_assets.py
```

This generates `examples/synthetic-comments.md` from a fixed, explicitly synthetic set. These examples are invented teaching material, not anonymized or paraphrased observations, and are not used to calculate the historical results.

## Historical scope and interpretation

The course report recorded 67 curated video targets and 6,137 retained comments. Its model labels were 35.8% neutral, 33.8% negative, and 30.4% positive. These are historical descriptive figures, not a representative estimate of Philippine opinion or a fresh reproduction. Raw observations are deliberately not supplied in this showcase.

The pipeline used English/Tagalog filtering, CardiffNLP's `twitter-xlm-roberta-base-sentiment`, and exploratory K-means clustering of TF-IDF/LSA features. Model sentiment is not a validated measure of cultural ownership, authenticity, or nationalism. Code-switching, sarcasm, model-domain mismatch, curated/high-engagement sampling, uneven reply coverage, and repeated authors can affect interpretation. Topic labels were informal interpretations, not validated research findings. No local sentiment gold set, sampling uncertainty, or causal analysis is claimed.

## Data and publication boundary

Identifiable comment excerpts, creator/target registries, copied videos, editor-guide quote banks, and unreviewed derived images have been removed from the candidate tree. The historical generator that redistributed excerpts has been replaced with the synthetic demonstration. Local analysis outputs now go under ignored `data/derived/`; removing a handle alone does not anonymize searchable text.

This is a **current-tree correction**. Earlier commits and external copies may still contain the removed material. The repository is withheld from public CV/profile linking pending verified history remediation and final permissions/privacy review. See [privacy and artifact notes](docs/privacy.md). No legal clearance or complete historical erasure is claimed.

The original scraper is retained as archived coursework code, without a supplied target list or a recommendation to resume collection. New collection and redistribution require their own justified purpose, applicable privacy/platform requirements, permissions, and safeguards. This maintenance did not scrape, download creator media, upload a documentary, or change an external course deliverable.

For historical local analysis, `pyproject.toml` describes the environment and notebooks 02–04 process separately held inputs. The corpus is not distributed and these results are not reproducible from the public repository alone. Keep observations, notebook outputs, credentials, generated reports, and media out of commits. Only reviewed aggregate releases and expressly synthetic examples belong in this showcase.

## License

The repository code is Apache-2.0; see [LICENSE](LICENSE). That license grants no rights to third-party comments, translations, images, or videos. No third-party media is included in the corrected showcase tree.
