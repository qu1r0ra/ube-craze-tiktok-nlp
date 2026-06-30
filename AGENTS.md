# Ube Craze NLP — Agent Index

**Start here for a new session:** [HANDOFF.md](HANDOFF.md) (workspace-wide living handoff).

Canonical project rules and data directories:

| Resource               | Path                                                                         |
| ---------------------- | ---------------------------------------------------------------------------- |
| **Workspace Handoff**  | [HANDOFF.md](HANDOFF.md)                                                     |
| Tech Stack Reference   | [.cursor/rules/tech-stack.mdc](.cursor/rules/tech-stack.mdc)                 |
| Project Overview Rules | [.cursor/rules/project-overview.mdc](.cursor/rules/project-overview.mdc)     |
| Data Registry          | [.cursor/project/data_registry.md](.cursor/project/data_registry.md)         |
| Analysis Registry      | [.cursor/project/analysis_registry.md](.cursor/project/analysis_registry.md) |
| Approved Proposal      | [references/proposal.md](references/proposal.md)                             |
| Source Layout          | `src/ube_craze_nlp/`                                                         |

**Conventions:**

1. Do not commit raw data stored in `data/` or generated figures in `outputs/`.
2. Ensure that code changes pass `ruff` check and format rules.
3. Keep code modular, separate concerns between scraper engine, DOM/JSON parser, cleaning utilities, and sentiment models.
