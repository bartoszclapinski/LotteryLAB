### Security, Performance, Observability

- **Security**:
  - Never commit secrets; use env vars via `src/utils/config.py`.
  - Sanitize error messages; log detailed context server-side only.
  - Plan rate limiting and access logs (future backlog) for public endpoints.
  - Validate and bound query params (`limit` caps, date ranges) to avoid abuse.
- **Performance**:
  - Index frequent filters (`draw_date`, `game_type`, consider composite).
  - Cache hot calculations later (Redis backlog); start with efficient SQL.
  - Avoid N+1; batch operations in ingestion; limit payload sizes.
- **Observability**:
  - Use rotating file logs (`.logs/`), UTC timestamps.
  - Add minimal structured fields in logs (key=value style) for grepability.
  - Keep `/api/v1/health` lightweight; optionally extend with DB check behind a flag.
