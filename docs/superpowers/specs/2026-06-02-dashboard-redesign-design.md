# Dashboard Redesign — Design Spec
**Date:** 2026-06-02  
**Status:** Approved  

---

## Goal

Redesign `docs/index.html` from a dark terminal/hacker aesthetic to a clean, airy, card-based light design inspired by typeui.sh. All existing data and functionality is preserved; only the visual presentation changes.

---

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Aesthetic direction | typeui.sh-inspired — clean, airy, light | Moves from "hacker console" to polished personal showcase |
| Font | Inter (Google Fonts) | Clean, modern sans-serif; replaces JetBrains Mono |
| Background | `#f5f5ff` (off-white with indigo tint) | Warm without being stark; subtle brand color |
| Primary accent | `#4f46e5` (indigo) | Consistent with bg tint; distinct from status colors |
| Status colors | Semantic, unchanged | green=live, yellow=building, blue=idea, etc. — users already know them |
| Layout | Card grid (reps) + sticky Field Notes sidebar on the right | Replaces left-panel journal + table; more visual, scannable |
| Card images | GitHub repo logo → `image` field in reps.yaml → letter avatar | Progressive — works today, improves as images are added |
| Constraints | Vanilla JS, single HTML file, static GitHub Pages, no build step | Unchanged from current site |

---

## Visual Design

### Color tokens
```css
--bg:        #f5f5ff;   /* page background */
--surface:   #ffffff;   /* card / panel background */
--border:    #e0e7ff;   /* card borders, dividers */
--border-dim:#f0f0ff;   /* inner dividers */
--accent:    #4f46e5;   /* indigo — links, active states, dates */
--accent-dim:#a5b4fc;   /* muted indigo — rep IDs, secondary labels */
--accent-bg: #ede9fe;   /* indigo tint — selected chips, hover states */
--text:      #1e1b4b;   /* near-black with indigo undertone */
--text-2:    #374151;   /* body text */
--text-3:    #6b7280;   /* secondary / metadata */
--shadow-sm: 0 1px 4px rgba(79,70,229,.06);
--shadow-md: 0 4px 16px rgba(79,70,229,.13);
```

### Typography
- Font: `Inter` (weights 400, 500, 600, 700, 800) via Google Fonts
- Page title: 26px / 800 weight / letter-spacing -0.5px
- Card name: 13px / 700
- Body / summary: 12–13px / 400–500
- Labels (uppercase): 10px / 700 / letter-spacing 0.08em

### Status badge colors (unchanged semantics, restyled as pill tags)
| Status | Background | Text |
|---|---|---|
| live | `#d1fae5` | `#065f46` |
| building | `#fef9c3` | `#92400e` |
| idea | `#ede9fe` | `#6d28d9` |
| assessed | `#f3f4f6` | `#374151` |
| pmf | `#fae8ff` | `#7e22ce` |
| dead | `#f3f4f6` | `#9ca3af` |

### Letter avatar gradients (fallback when no image)
Gradient direction: `135deg`. Colors keyed to status:
- live → `#059669 → #34d399`
- building → `#d97706 → #fbbf24`
- idea → `#4f46e5 → #a5b4fc`
- assessed → `#6b7280 → #9ca3af`
- pmf → `#7e22ce → #c084fc`
- dead → `#9ca3af → #d1d5db`

---

## Page Structure

```
┌─────────────────────────────────────────────────────┬──────────────┐
│  HEADER                                             │              │
│  Title + subhead                    20/100 ████░░  │              │
├─────────────────────────────────────────────────────┤  FIELD NOTES │
│  [All 20] [✓ Live 3] [⚙ Building 5] …   [Search]  │  SIDEBAR     │
├─────────────────────────────────────────────────────┤  (sticky,    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  280px)      │
│  │ image/av │  │ image/av │  │ image/av │          │              │
│  │ Rep name │  │ Rep name │  │ Rep name │          │  Apr 28      │
│  │ status   │  │ status   │  │ status   │          │  #002 #014   │
│  │ summary  │  │ summary  │  │ summary  │          │  preview…    │
│  │ next →   │  │ next →   │  │ next →   │          │              │
│  └──────────┘  └──────────┘  └──────────┘          │  Apr 27      │
│  ┌─────────────────────────────────────────────┐   │  #014        │
│  │ DETAIL EXPANDER (full grid width)           │   │  preview…    │
│  │ [avatar] Name  Rep 00N · PITA N · Last: date│   │              │
│  │─────────────────────────────────────────────│   │              │
│  │ Summary / Next Step / Links │ Field Notes   │   │              │
│  │                             │ Timeline      │   │              │
│  └─────────────────────────────────────────────┘   │              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │              │
│  │  card    │  │  card    │  │  card    │          │              │
└──┴──────────┴──┴──────────┴──┴──────────┴──────────┴──────────────┘
```

### Header
- Title: `100 Reps Project` — large, 800 weight
- Subhead: tagline linking to Substack
- Progress: `20 / 100` in accent color + slim rounded progress bar (indigo gradient fill)

### Filter row
- Status filter pills: rounded-full pill buttons, one per status + "All"
- Active pill: solid indigo with shadow
- Inactive pills: tinted by status color (same semantic colors as badges)
- Search input: right-aligned, rounded, indigo focus ring

### Card grid
- 3 columns desktop (≥1024px), 2 columns tablet (640–1023px), 1 column mobile (<640px)
- `gap: 14px`
- Each card:
  - **Image area** (90px tall): repo logo image, Unsplash/screenshot from `image` field, or letter avatar gradient
  - **Body**: Rep ID (muted indigo, uppercase) + status badge | Name (700 weight) | Summary (muted) | Next step (indigo, `→` prefix, shown when not null)
  - Hover: lift + stronger shadow
  - Selected (expanded): indigo border ring

### Detail expander
Rendered as a `grid-column: 1 / -1` grid child interleaved between card elements — `renderCardGrid()` outputs cards and the expander in a single flat list, inserting the expander after the last card in the same visual row as the selected card. Animates in with a subtle slide-down.

- **Header bar**: image/avatar (48×48, rounded-10) + name + rep ID / PITA / last action + status badge + close (✕) button
- **Body** — two-column layout:
  - **Left**: Summary → Next Step → Links (as chip tags with icons)
  - **Right**: Field Notes (date + preview, up to 5, clickable to expand) + Timeline (commits + milestones, scrollable, "show N more" toggle)
- Blocker section (red, bold) shown when `blocker` is not null — between Summary and Next Step

### Field Notes sidebar
- Position: right side, sticky, `max-height: calc(100vh - 48px)`, scrollable
- Width: 280px (collapses to a narrow rail on mobile — same behavior as current left panel but mirrored)
- Each entry: date (accent), rep chips (indigo pill, click scrolls to that card), tag chips (gray), preview text
- Newest entry shows full body; older entries show preview, expand on click
- Stale dot indicator if no entry in >3 days (unchanged from current)
- Tabs: Notes (active) | Lessons → (links to lessons.html)

---

## Image Loading Logic

Executed per card at render time. Results cached in memory (no repeated fetches).

```
fetchRepImage(rep):
  1. If rep.image exists → use it (relative path or URL)
  2. Else if rep.repo exists:
       try https://raw.githubusercontent.com/{repo}/HEAD/logo.png
       try https://raw.githubusercontent.com/{repo}/HEAD/logo.svg
       try https://raw.githubusercontent.com/{repo}/HEAD/logo.jpg
       try https://raw.githubusercontent.com/{repo}/HEAD/public/logo.png
       try https://raw.githubusercontent.com/{repo}/HEAD/assets/logo.png
     → use first that returns 200
  3. Else → render letter avatar (first letter of rep name, gradient by status)
```

Image elements use `onerror` chaining to fall through to the next candidate, then to the avatar. All fetches are lazy (triggered when the card renders into view or on initial render) and cached by rep ID.

### reps.yaml change
One new **optional** field per rep, after `repo`:
```yaml
image: docs/images/002.jpg        # relative path to stored screenshot
# or
image: https://example.com/logo.png  # any public URL
```
Omit entirely if no image. Default behavior (GitHub logo lookup → avatar) applies when absent. Existing reps require no changes.

---

## JavaScript Changes

### Removed
- `renderTable()` — table-based rendering
- `renderCards()` — old mobile card fallback
- View toggle button (table ↔ cards)
- `viewMode` state variable

### Added
- `renderCardGrid(filtered)` — renders 3-col card grid with letter avatars and image loading
- `renderDetailExpander(rep)` — builds the full-width detail panel HTML (summary, next step, blocker, field notes, timeline, links)
- `fetchRepImage(rep)` — image resolution chain described above
- `imageCache` — object keyed by rep ID, stores resolved image URL or `null` (avatar)
- `insertDetailAfterRow(repId)` — DOM helper that finds the grid row containing the selected card and inserts the expander after it

### Unchanged (zero modifications)
- `fetchData()`, `simpleHash()`, YAML parsing
- `fetchGitHistory()`, `mergeTimelines()`, `renderTimelineEntries()`
- `fetchFieldNotes()`, `renderJournal()`, `fieldNotesForRep()`
- `sanitizeNextStep()`, `esc()`, `truncate()`
- `getFilteredSorted()`, `setFilter()`, `setSort()`
- All keyboard navigation event handlers
- `computeLastActions()`, auto-refresh interval
- `wireJournalChrome()` (panel collapse/expand, localStorage)
- `pitaColor()` (still used in detail header)

---

## lessons.html
Gets a matching light theme update in the same PR: same CSS tokens, Inter font, indigo accents. No structural or data changes.

---

## Build & Delivery

1. Create `docs/index-v2.html` — develop and preview locally with `npm run dev`
2. Verify feature parity checklist before swapping:
   - [ ] All 20 reps render with correct status/PITA/badges
   - [ ] Filter pills work (all statuses + ALL)
   - [ ] Search filters correctly
   - [ ] Keyboard nav (j/k/Enter/Esc/?/0-6) works
   - [ ] Expand/collapse detail panel works
   - [ ] Timeline loads and shows git commits + milestones
   - [ ] Field notes render in sidebar and in detail panel
   - [ ] Journal collapse/expand persists in localStorage
   - [ ] Rep chips in journal scroll to correct card
   - [ ] Image loading: logo found → shown; logo missing → letter avatar
   - [ ] `lessons.html` light theme matches
   - [ ] Mobile layout (2-col → 1-col grid, journal as overlay rail)
   - [ ] `REPS_YAML_SPEC.md` updated to document optional `image` field
3. Rename `index-v2.html` → `index.html`, delete old file, commit

---

## Out of Scope
- Dark mode toggle
- Server-side rendering or build step
- Automated screenshot capture (manual or agent task; `image` field populated over time)
- Changes to `reps.yaml` schema beyond the optional `image` field
- Changes to the build pipeline (`scripts/build_journal.py`, CI workflows)
