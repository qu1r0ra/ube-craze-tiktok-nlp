# Ube Craze NLP — Agent Index

| Resource              | Path                                                                         |
| :-------------------- | :--------------------------------------------------------------------------- |
| **Workspace Handoff** | [HANDOFF.md](HANDOFF.md)                                                     |
| Tech Stack Reference  | [.agents/rules/tech-stack.md](.agents/rules/tech-stack.md)                   |
| Project Overview      | [.agents/rules/project-overview.md](.agents/rules/project-overview.md)       |
| Data Registry         | [.agents/project/data_registry.md](.agents/project/data_registry.md)         |
| Analysis Registry     | [.agents/project/analysis_registry.md](.agents/project/analysis_registry.md) |
| Approved Proposal     | [docs/proposal.md](docs/proposal.md)                                         |

**Conventions:**

1. **No Raw Data Commits**: Keep `data/` ignored; commit figures & summaries in `outputs/`.
2. **Relative Links Only**: Use relative paths in markdown links (no absolute `file:///` URLs).
3. **Windows Encoding**: Run Python commands with `$env:PYTHONIOENCODING="utf-8";` on Windows.
4. **No Emojis in Code**: Emojis are forbidden in Python code/logs (permitted only in parser tests).
5. **Logging over Print**: Use standard module-level `logging` (`logger = logging.getLogger(__name__)`).
