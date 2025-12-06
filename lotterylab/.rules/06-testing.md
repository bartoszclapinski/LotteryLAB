### Testing Rules (pytest)

- **Scope**: Unit tests for parsing, validation, analysis; integration tests for repositories and API where applicable.
- **Layout**: Keep tests in `lotterylab/tests/`; mirror module names (`test_file_parser.py`, etc.).
- **Fixtures**:
  - Use `tests/conftest.py` for shared fixtures (DB session, sample data).
  - Prefer in-memory or temp SQLite DB for isolated tests.
- **Isolation**:
  - No cross-test state. Clean up DB after tests; use transactions/rollbacks.
- **Assertions**:
  - Prefer precise assertions on both values and shapes (lengths, keys).
  - For statistical tests, assert ranges (e.g., p-value within tolerance) rather than exact floats.
- **Coverage**:
  - Target 80%+ overall. Ensure core analysis, ingestion, and repositories are covered.
- **Performance**:
  - Keep tests < 2s each; use small synthetic datasets.
- **Naming**:
  - Test names describe behavior: `test_validate_draw_rejects_future_date`.
- **CI-readiness**:
  - Tests must be deterministic; seed random generators if used.
