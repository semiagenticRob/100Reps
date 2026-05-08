# Rep 021 — n-of-one

**Status:** Building
**Repo:** [semiagenticRob/n-of-one-template](https://github.com/semiagenticRob/n-of-one-template)

Personal health intelligence tool. Aggregates multiple self-tracked data sources to surface n-of-1 insights — patterns specific to the individual, not population averages.

## Data Sources

| Source | Method |
|--------|--------|
| Strava | OAuth API (automated) |
| Coros watch | API / export |
| Weight | Manual via Telegram check-in |
| Peptides / supplements | Manual via Telegram check-in |
| Mood | Scheduled Telegram prompt |
| Nutrition | Daily quality score 1–5 (low friction) |

## Next Steps

- Define MVP data model
- Strava API integration (automated workout pull)
- Daily Telegram check-in UX (mood + weight + diet score)
- Weekly AI-generated insight report

## Milestones

- 2026-05-07: Rep conceived — brainstorm session. Repo created.
- 2026-05-07: Moved to building — full technical spec written.
