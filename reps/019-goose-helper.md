# Rep 019 — Goose Helper

**Status:** Building
**Repo:** [semiagenticRob/goose-helper](https://github.com/semiagenticRob/goose-helper)

Business intelligence dashboard for an executive at a wildfowl mitigation company. Labor utilization view — confirmed billable, unmapped probable, and non-billable hours broken out by team and person, with week/month/quarter toggle. Built in React/TypeScript/Vite.

## Next Steps

- Send client data onboarding questions from `docs/superpowers/specs/client-data-onboarding.md` to WGC Bird contact — fastest path is requesting a single ADP CSV export to replace mock data
- Pipeline architecture spec in `docs/superpowers/specs/zoho-adp-data-pipeline-spec.md` — ADP and Zoho API details + CSV fallback path
- Add geography/team view distinguishing Core Services (IL, WI, Detroit, Indy) vs. Structural division

## Deliverables

- `docs/superpowers/specs/zoho-adp-data-pipeline-spec.md` — API requirements, data schemas, CSV fallback path
- `docs/superpowers/specs/client-data-onboarding.md` — 15 intake questions for ADP access, Zoho setup, team roster, deployment. Includes minimal request to send client today.

## Milestones

- 2026-04-22: Repo created — React/TypeScript/Vite prototype with mock data. Company-level and team-level cards, utilization thresholds, per-person breakdowns.
- 2026-04-22: WGC Bird deep-dive call — team structure confirmed (Core Services + Structural), data pipeline: proprietary app → Zoho → ADP. Built drill-down and team expansion views live on call.
- 2026-04-23: CEO Agent — Zoho/ADP data pipeline spec authored. ADP Workforce Now API + Zoho Books/Projects API requirements, MVP data schema, CSV export fallback path. Saved to docs/superpowers/specs/zoho-adp-data-pipeline-spec.md.
- 2026-04-24: CEO Agent — Client data onboarding guide authored. 15 intake questions (ADP product/access, Zoho time tracking, team roster, deployment preferences) + minimum viable request to send client now. Saved to docs/superpowers/specs/client-data-onboarding.md.
