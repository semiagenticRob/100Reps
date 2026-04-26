# Rep 019 — Goose Helper

**Status:** Building
**Repo:** [semiagenticRob/goose-helper](https://github.com/semiagenticRob/goose-helper)

Business intelligence dashboard for an executive at a wildfowl mitigation company. Labor utilization view — confirmed billable, unmapped probable, and non-billable hours broken out by team and person, with week/month/quarter toggle. Built in React/TypeScript/Vite.

## Next Steps

- Send 3-doc bundle to WGC Bird contact:
  1. `docs/superpowers/specs/client-executive-brief.md` — business-terms overview, 3 dashboard views, data options
  2. `docs/superpowers/specs/client-data-onboarding.md` — 15 intake questions
  3. `docs/superpowers/specs/data-mapping-template.md` — fillable roster + job code mapping + hours thresholds
- Request one ADP CSV export as fastest path to live data (instructions in data-mapping-template.md)
- Pipeline architecture spec in `docs/superpowers/specs/zoho-adp-data-pipeline-spec.md` — reference for API setup once credentials shared

## Deliverables

- `docs/superpowers/specs/zoho-adp-data-pipeline-spec.md` — ADP/Zoho API requirements, data schemas, CSV fallback path
- `docs/superpowers/specs/client-data-onboarding.md` — 15 intake questions for ADP access, Zoho setup, team roster, deployment
- `docs/superpowers/specs/client-executive-brief.md` — one-pager: what the dashboard does, 3 views (company/team/person), two data options (API vs CSV), data-sharing ask
- `docs/superpowers/specs/data-mapping-template.md` — fillable roster table, job code → utilization category mapping, hours targets, ADP export instructions, deployment preference questions

## Milestones

- 2026-04-22: Repo created — React/TypeScript/Vite prototype with mock data. Company-level and team-level cards, utilization thresholds, per-person breakdowns.
- 2026-04-22: WGC Bird deep-dive call — team structure confirmed (Core Services + Structural), data pipeline: proprietary app → Zoho → ADP. Built drill-down and team expansion views live on call.
- 2026-04-23: CEO Agent — Zoho/ADP data pipeline spec authored. ADP Workforce Now API + Zoho Books/Projects API requirements, MVP data schema, CSV export fallback path. Saved to docs/superpowers/specs/zoho-adp-data-pipeline-spec.md.
- 2026-04-24: CEO Agent — Client data onboarding guide authored. 15 intake questions + minimum viable request to send client now. Saved to docs/superpowers/specs/client-data-onboarding.md.
- 2026-04-25: CEO Agent — Client executive brief authored. One-pager for WGC Bird data-sharing conversation: what dashboard does, 3 views, API vs CSV options, clear ask. Saved to docs/superpowers/specs/client-executive-brief.md.
- 2026-04-26: CEO Agent — Data mapping template authored. Fillable roster, job code → utilization mapping, hours thresholds, ADP export instructions. Saved to docs/superpowers/specs/data-mapping-template.md.
