# Rep 017 — Solar Miner

**Status:** Building
**Repo:** [semiagenticRob/solar-miner](https://github.com/semiagenticRob/solar-miner)

Throttle two Bitmain Antminer S19s to consume only surplus rooftop solar production via Braiins OS+ and Enphase API. Zero incremental grid cost — converts electricity that would otherwise export at low Xcel credit rates into Bitcoin.

## Architecture

Python daemon on an always-on Mac reads real-time solar production from Enphase IQ Gateway, estimates house consumption from Xcel billing data, calculates surplus, and dynamically sets power targets on the S19s via Braiins REST API. Safety layer ensures miners never draw from the grid.

## Hardware

- 2x Bitmain Antminer S19 (owned)
- Enphase solar inverter system (installed)
- Braiins OS+ firmware
- Garage placement, 240V circuit

## Milestones

- 2026-04-11: Rep conceived and brief written
- 2026-04-13: Repo created, implementation plan finalized

## Next Steps

- Get Enphase IQ Gateway API token (local network access)
- Download Xcel interval data for consumption profile
- Flash Braiins OS+ on both S19s and calibrate power throttle range
- Build the control daemon
