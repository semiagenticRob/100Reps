# Rep 017 — Solar Miner

**Status:** Dead
**Repo:** [semiagenticRob/solar-miner](https://github.com/semiagenticRob/solar-miner)

Two Bitmain S19 miners throttled automatically to consume only excess rooftop solar production. Monetizes otherwise wasted electricity with zero incremental grid cost.

**Killed 2026-04-13:** Net metering is not revenue-generating; model does not work under current net metering structure. Revisit only if heating component added.

## Architecture

Python daemon on an always-on Mac reads real-time solar production from Enphase IQ Gateway, estimates house consumption from Xcel billing data, calculates surplus, and dynamically sets power targets on the S19s via Braiins REST API. Safety layer ensures miners never draw from the grid.

## Hardware

- 2x Bitmain Antminer S19 (owned)
- Enphase solar inverter system (installed)
- Braiins OS+ firmware
- Garage placement, 240V circuit

## Milestones

- 2026-04-11: Rep conceived and brief written
- 2026-04-13: Repo created, daemon implemented, Xcel billing profiles built, IQ Gateway found at 192.168.0.38
- 2026-04-13: Killed — net metering not revenue-generating, model broken
