### Database, SQLAlchemy, Alembic

- **Models**: Define in `src/database/models.py`; keep columns explicit; use `Mapped` types.
- **Session**: Use `SessionLocal` from `src/database/session.py`; never keep sessions global.
- **Migrations**:
  - Alembic revisions already present; one change per revision with descriptive message.
  - Autogenerate then review; ensure indexes are included when needed.
  - Don’t edit past migrations.
- **Indexes**:
  - Ensure `draws(draw_date)` and `draws(game_type)` exist (done). Consider composite for frequent filters.
- **Data integrity**:
  - Validate ranges at app level; DB constraints where safe.
- **Performance**:
  - Use `select()` with filters; avoid loading large result sets unnecessarily.
  - Repository pattern for query reuse (`src/repositories/`).
- **SQLite vs Postgres**:
  - Default dev: SQLite `lotterylab.db`. Plan for Postgres in prod; avoid vendor-specific SQL.
