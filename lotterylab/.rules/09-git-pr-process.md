### Git and PR Process

- **Branches**:
  - `main` is stable; feature work on `feature/*`, fixes on `fix/*`.
- **Commits**:
  - Small, focused; imperative mood: "Add chi-square endpoint".
  - Reference issue/sprint item when applicable.
- **PRs**:
  - Keep scope tight; include description, acceptance criteria, and screenshots for UI.
  - Link to relevant PRD section/backlog item; note risks/assumptions.
  - Request review; address comments promptly.
- **Migrations**:
  - Include alembic revision SQL in the PR description if impactful.
- **Checks**:
  - Tests must pass; lints clean; run locally before pushing.
- **Changelog/Log**:
  - Update `sprints/log.md` with key milestones (date, summary).
