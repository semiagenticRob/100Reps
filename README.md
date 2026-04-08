# The 100 Reps Project

100 product launches. A couple become real businesses. The number is a method, not a goal — volume creates the conditions for something to break through.

## Status

**Progress: 13 / 100** — 1 dead, 2 live, 3 building, 7 idea/bench/validating

| Status | Meaning |
|--------|---------|
| Idea | Not yet assessed |
| Assessed | Evaluated, not yet building |
| Building | Active development |
| Live | Shipped, in market |
| PMF | Money in the door |
| Dead | Closed at any stage |

## Active Reps

| Rep | Project | Status | Tier | Repo |
|-----|---------|--------|------|------|
| 002 | Estate Sale Helper | Live | Active | [estate-sale-helper](https://github.com/semiagenticRob/estate-sale-helper) |
| 006 | Teshuvah Read Along | Building | Active | [teshuvah-read-along](https://github.com/semiagenticRob/teshuvah-read-along) |

## Bench

| Rep | Project | Status | Repo |
|-----|---------|--------|------|
| 003 | Stack Tracker | Building | [stack-tracker](https://github.com/semiagenticRob/stack-tracker) |
| 005 | Route Mapper | Building | [cardio-route-finder](https://github.com/semiagenticRob/cardio-route-finder) |
| 009 | Colorado Totes | Validating | — |
| 012 | STR Intel | Building | — |
| 013 | Civic Transparency Tool | Assessed | [civic-transparency-tool](https://github.com/semiagenticRob/civic-transparency-tool) |

## Validating

| Rep | Project | Status | Repo |
|-----|---------|--------|------|
| 011 | myvoiceprofile.com | Live | [myvoiceprofile](https://github.com/semiagenticRob/myvoiceprofile) |

## Idea Pool

| Rep | Project | Notes |
|-----|---------|-------|
| 004 | Runtime | Paused |
| 007 | WritersRoom.ai | Paused — service business |
| 008 | Declutter Truck | Paused |
| 010 | AI Diary | Blocked on Stack Tracker |

## Dead

| Rep | Project | Notes |
|-----|---------|-------|
| 001 | Pipe Acquisition | Did not proceed |

---

## Architecture

- **State**: `reps.yaml` is the single source of truth
- **Narrative**: Obsidian vault (RW Vault) holds research, analysis, and dated logs per rep
- **Execution**: Paperclip agents build and research reps, committing to individual repos
- **Monitoring**: NanoClaw watches GitHub activity and provides Telegram interface
- **Per-rep details**: See `reps/` directory
