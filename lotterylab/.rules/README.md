### Lottery Lab — Project Rules (for Cursor/LLMs)

- **Scope**: Coding standards, API/UI patterns, DB/migrations, data ingestion, testing, security/performance, collaboration with LLMs, PR process, branding/theming.
- **Applies to**: All contributors and AI assistants (Cursor, GPT-family, Claude, etc.).
- **Principles**: Scientific rigor, clarity, incremental delivery, safety by default, Python-first.

- **Files** (lotterylab/.rules/):
  - `01-coding-python.md` — Python coding standards and structure
  - `02-api-fastapi.md` — API design, versioning, schemas
  - `03-frontend-jinja-htmx.md` — Jinja/HTMX/Plotly UI rules
  - `04-database-sqlalchemy-alembic.md` — models, migrations, indexes
  - `05-data-ingestion.md` — parsing, validation, scheduler, audit
  - `06-testing.md` — pytest layout, fixtures, DB tests
  - `07-security-performance.md` — security, perf, observability
  - `08-cursor-llm-collab.md` — how AI should operate in this repo
  - `09-git-pr-process.md` — commits, PRs, reviews
  - `10-branding-theming.md` — UI tokens, light/dark, assets

- **Cursor Rules** (.cursor/rules/):
  - `project-lottery-lab.mdc` — Project-specific guidelines, educational focus, performance targets

- **References**:
  - PRD: `lotterylab/.ai/lotto-analysis-prd.md`
  - Sprints: `lotterylab/.ai/sprints/`
  - Design: `.design/` (UI/UX source of truth)

Follow the per-file rules; when in doubt, prefer clarity and tests over cleverness.
