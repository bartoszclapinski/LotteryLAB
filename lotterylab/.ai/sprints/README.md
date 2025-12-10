# 🧪 Lottery Lab Sprints

Welcome! This folder holds the iterative delivery plan for Lottery Lab, aligned with the PRD in `lotterylab/.ai/lotto-analysis-prd.md`. The plan is research-focused, educational, and emphasizes statistical rigor.

## 🚀 Quick Start for New LLMs

**Start here:** Read `../.ai/ONBOARDING.md` for comprehensive project onboarding!

## 📁 Structure
- `../ONBOARDING.md` — 🆕 **LLM onboarding guide** (start here!)
- `ROADMAP.md` — high-level multi-sprint plan and milestones
- `BACKLOG.md` — prioritized product backlog derived from the PRD
- `_sprint_template.md` — reusable template for new sprints
- `sprint000/plan.md` — pre-API-key kickoff sprint ✅
- `sprint001/plan.md` — MVP delivery sprint ✅
- `sprint002/plan.md` — Core analyses sprint ✅
- `sprint003/plan.md` — ML baseline sprint 📋
- `log.md` — running log of sprint planning updates

## 📊 Current Status (2025-12-10)
| Sprint | Status | Description |
|--------|--------|-------------|
| 000 | ✅ Done | Scaffolding, DB, CSV import |
| 001 | ✅ Done | MVP (UI, API, frequency) |
| 002 | ✅ Done | Randomness, patterns, correlation, trends, export, i18n |
| 003 | 📋 Next | ML baseline (educational) |

## 🤝 Working agreements
- Keep changes small and commit frequently ✅
- Update `log.md` when plans change 🔁
- Prefer measurable acceptance criteria 🎯
- Track risks early; add mitigations ⚠️
- Use clear emojis for readability (but keep it professional) 🙂

## 🔤 Emoji legend
- 🚀 Goal/Mission
- ✅ Acceptance criteria / Done
- 📦 Deliverable
- 🔧 Task/Implementation
- 🧪 Tests / Validation
- 📊 Metrics / KPIs
- ⚠️ Risk / Mitigation
- 🗺️ Scope / Boundaries
- 🔁 Change / Iteration

## 🧭 How to add a new sprint
1. Copy `_sprint_template.md` to `sprintXYZ/plan.md` 🔧
2. Fill in Dates, Goal, Scope, Deliverables, Stories, Tasks, Risks, Metrics ✅
3. Link new sprint from `ROADMAP.md` and reference any new backlog items 🔗
4. Add an entry in `log.md` 📓

## 🔗 References
- **Onboarding**: `../.ai/ONBOARDING.md` ← Start here!
- **PRD**: `../.ai/lotto-analysis-prd.md`
- **Math methods**: `../.ai/mathematical-methods.md`
- **Design mockup**: `../.design/main-design-1.1.html`
- **Tech stack**: Python 3.11+, FastAPI (Jinja2+HTMX), SQLAlchemy, Pandas/NumPy/SciPy, Plotly
