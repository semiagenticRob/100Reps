# Rep 030 — I Am Not A Trader, Bot

**Status:** Building
**Repo:** [semiagenticRob/i-am-not-a-trader-bot](https://github.com/semiagenticRob/i-am-not-a-trader-bot)

Evidence-gated Polymarket BTC 5-minute trading system. Strategies trade on paper, earn capital only after clearing a statistical funding gate, then evolve via champion/challenger promotion.

## Next Steps

- Run shadow mode to accumulate 100+ trades toward the funding gate, then work through the Phase 2 runbook before any real capital trades

## Milestones

- 2026-07-15: Rep conceived — AI and trading intersection project. Repo created at github.com/semiagenticRob/i-am-not-a-trader-bot.
- 2026-07-15: Design spec approved — evidence-gated architecture: STRATEGY.md source of truth, deterministic engine, shadow mode, statistical funding gate, champion/challenger evolution.
- 2026-07-16: Full engine (U1-U11) built, 12-persona code-reviewed, and merged to main via PR #1. Live trading remains gated behind a manual venue-decision step.
