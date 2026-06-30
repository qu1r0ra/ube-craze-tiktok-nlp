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
| Approved Proposal      | [docs/proposal.md](docs/proposal.md)                                         |
| Source Layout          | `src/ube_craze_nlp/`                                                         |

**Conventions:**

1. Do not commit raw data stored in `data/`. However, commit final generated figures and qualitative summaries in `outputs/` to preserve analytical visual artifacts.
2. Ensure that code changes pass `ruff` check and format rules.
3. Keep code modular, separate concerns between scraper engine, DOM/JSON parser, cleaning utilities, and sentiment models.
4. **Relative Links Only:** Keep all document links (e.g., within HANDOFF.md, AGENTS.md, or project registries) relative. Absolute local file:/// paths must not be used.
5. **Console Encoding (Windows):** Always run python execution commands prefixed with `$env:PYTHONIOENCODING="utf-8";` on Windows to avoid UnicodeEncodeError when printing emoji-heavy comments.
6. **No Emojis in Code:** Emojis must not be used in code files (such as logs, print statements, or code comments). They are only permitted where necessary for parsing raw data/emojis, or in specific test cases.
7. **Use Logging instead of Print:** Use Python's built-in `logging` module and configure `logger = logging.getLogger(__name__)` for all module scripts and library files rather than invoking `print()` directly.
