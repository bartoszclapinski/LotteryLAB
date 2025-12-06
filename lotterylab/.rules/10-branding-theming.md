### Branding and Theming Rules

- **Identity**:
  - Project name: "Lottery Lab". Tagline: "Where Luck Meets Science".
  - Educational/research positioning; avoid predictive claims.
- **Design tokens**:
  - Use CSS variables defined in `static/css/main.css`.
  - Light theme default; support dark mode via `html[data-theme="dark"]` tokens.
- **Components**:
  - Header with logo mark and tabs; three-column layout (sidebar, main, right panel).
  - Cards, tables, and chart containers follow existing CSS classes.
- **Assets**:
  - Favicon at `static/favicon.svg`. Keep SVG small and optimized.
- **Consistency**:
  - No inline styles; update CSS only in the stylesheet.
  - When adding new components, extend tokens first; then styles.
