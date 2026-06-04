# Dashboard Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `docs/index.html` as a clean, airy, card-based light-theme dashboard (Inter font, indigo accent, 3-col card grid, right-side journal sidebar) while preserving all existing data, JS logic, and interactivity.

**Architecture:** Create `docs/index-v2.html` alongside the live file. Replace the CSS block and HTML shell; rewrite only the rendering functions (`renderTable`/`renderCards` → `renderCardGrid`/`renderDetailExpander`); keep all data-loading, filtering, sorting, keyboard nav, and journal logic untouched. Verify locally then rename to replace `index.html`.

**Tech Stack:** Vanilla JS (ES5), js-yaml CDN, Inter via Google Fonts, static GitHub Pages. No build step. Run `npm run dev` (http-server on port 3000) to preview.

---

## File Map

| File | Action | What changes |
|---|---|---|
| `docs/index-v2.html` | Create | New file — full redesign built here |
| `docs/index.html` | Replace (Task 9) | Swapped out for index-v2.html at end |
| `docs/lessons.html` | Modify (Task 8) | CSS tokens + font only |
| `REPS_YAML_SPEC.md` | Modify (Task 9) | Document optional `image` field |

---

## Task 1: Create index-v2.html with new CSS + font

**Files:**
- Create: `docs/index-v2.html`

The first step copies the live file and replaces only the `<style>` block and font link. All HTML and JS stay identical. This gives a working baseline to verify before touching any logic.

- [ ] **Step 1: Copy index.html to index-v2.html**

```bash
cp docs/index.html docs/index-v2.html
```

- [ ] **Step 2: Swap the font link**

In `docs/index-v2.html`, find and replace the two `<link rel="preconnect">` lines and the Google Fonts `<link>`:

Old:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```

New:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

- [ ] **Step 3: Replace the entire `<style>` block**

Delete everything between `<style>` and `</style>` (inclusive) and replace with:

```html
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f5f5ff;--surface:#fff;--border:#e0e7ff;--border-dim:#f0f0ff;
  --accent:#4f46e5;--accent-dim:#a5b4fc;--accent-bg:#ede9fe;
  --text:#1e1b4b;--text-2:#374151;--text-3:#6b7280;
  --shadow-sm:0 1px 4px rgba(79,70,229,.06);
  --shadow-md:0 4px 16px rgba(79,70,229,.13);
  --font:'Inter',system-ui,sans-serif;
  --panel-w:280px;--rail-w:32px;
}
html,body{background:var(--bg);color:var(--text);font-family:var(--font);font-size:13px;line-height:1.5;overflow-x:hidden}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}

/* HEADER */
.header{padding:24px 24px 0}
.header-top{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;margin-bottom:16px}
.brand-title{font-size:26px;font-weight:800;color:var(--text);letter-spacing:-.5px;line-height:1.1}
.header-sub{font-size:13px;color:var(--text-3);margin-top:4px}
.header-sub a{color:var(--accent)}
.progress-area{display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.progress-label{font-size:13px;font-weight:700;color:var(--accent)}
.progress-track{height:6px;width:220px;background:var(--border);border-radius:999px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--accent),#818cf8);border-radius:999px;transition:width .5s ease}
.last-updated{font-size:11px;color:var(--text-3);text-align:right;padding:4px 24px 0}
.last-updated .feed-flash{color:var(--accent);opacity:0;transition:opacity .3s}
.last-updated .feed-flash.show{opacity:1}

/* FILTER ROW */
.filter-row{padding:14px 24px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.filter-pill{padding:6px 14px;border-radius:999px;font-size:12px;font-weight:600;cursor:pointer;border:none;font-family:var(--font);transition:all .15s;user-select:none}
.filter-pill:hover{filter:brightness(.95)}
.filter-pill.active{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(79,70,229,.25)}
.search-wrap{margin-left:auto;display:flex;align-items:center;gap:8px}
.search-wrap label{font-size:12px;color:var(--text-3)}
.search-input{padding:6px 12px;border-radius:8px;border:1px solid var(--border);background:var(--surface);font-family:var(--font);font-size:12px;color:var(--text);outline:none;width:180px}
.search-input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(79,70,229,.1)}

/* ERROR BANNER */
.error-banner{display:none;padding:10px 24px;background:#dc2626;color:#fff;font-weight:700;text-align:center;font-size:12px}
.error-banner.show{display:block}

/* APP SHELL */
.app-shell{display:flex;align-items:flex-start;gap:20px;padding:0 24px 60px}
.grid-col{flex:1;min-width:0}

/* CARD GRID */
.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:14px 0}
.rep-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow-sm);cursor:pointer;transition:box-shadow .15s,transform .15s,border-color .15s}
.rep-card:hover{box-shadow:var(--shadow-md);transform:translateY(-1px)}
.rep-card.selected{border-color:var(--accent);box-shadow:0 0 0 2px rgba(79,70,229,.2),var(--shadow-md);transform:translateY(-1px)}
.rep-card.dead-card{opacity:.5}
.rc-image{width:100%;height:90px;object-fit:cover;display:block}
.rc-avatar{width:100%;height:90px;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800;color:#fff;letter-spacing:-1px;flex-shrink:0}
.rc-body{padding:12px 14px 14px}
.rc-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}
.rc-id{font-size:10px;font-weight:600;color:var(--accent-dim);text-transform:uppercase;letter-spacing:.05em}
.rc-tag{padding:2px 8px;border-radius:999px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;display:inline-block}
.rc-name{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px;line-height:1.3}
.rc-summary{font-size:11px;color:var(--text-3);line-height:1.45}
.rc-next{margin-top:9px;padding-top:9px;border-top:1px solid var(--border-dim);font-size:11px;color:var(--accent);display:flex;gap:4px;align-items:flex-start}
.rc-stale{font-size:9px;color:#d97706;margin-left:4px}

/* STATUS tag colors */
.tag-idea{background:#ede9fe;color:#6d28d9}
.tag-assessed{background:#f3f4f6;color:#374151}
.tag-building{background:#fef9c3;color:#92400e}
.tag-live{background:#d1fae5;color:#065f46}
.tag-pmf{background:#fae8ff;color:#7e22ce}
.tag-dead{background:#f3f4f6;color:#9ca3af}

/* AVATAR gradients by status */
.av-idea{background:linear-gradient(135deg,#4f46e5,#a5b4fc)}
.av-assessed{background:linear-gradient(135deg,#6b7280,#9ca3af)}
.av-building{background:linear-gradient(135deg,#d97706,#fbbf24)}
.av-live{background:linear-gradient(135deg,#059669,#34d399)}
.av-pmf{background:linear-gradient(135deg,#7e22ce,#c084fc)}
.av-dead{background:linear-gradient(135deg,#9ca3af,#d1d5db)}

/* DETAIL EXPANDER */
.detail-bridge{grid-column:1/-1;background:var(--surface);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow-md);overflow:hidden;animation:slideDown .18s ease}
@keyframes slideDown{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}
.detail-header{display:flex;align-items:center;gap:14px;padding:16px 20px;border-bottom:1px solid var(--border-dim);background:#fafaff;flex-wrap:wrap}
.dh-thumb{width:48px;height:48px;border-radius:10px;object-fit:cover;flex-shrink:0}
.dh-thumb-av{width:48px;height:48px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:#fff;flex-shrink:0}
.dh-name{font-size:16px;font-weight:800;color:var(--text);line-height:1.2}
.dh-meta{font-size:11px;color:var(--text-3);margin-top:2px}
.dh-tag{margin-left:auto}
.dh-close{margin-left:8px;background:none;border:none;color:var(--accent-dim);font-size:18px;cursor:pointer;padding:4px 8px;border-radius:6px;line-height:1;font-family:var(--font)}
.dh-close:hover{background:var(--accent-bg);color:var(--accent)}
.detail-body{display:grid;grid-template-columns:1fr 1fr}
.detail-col{padding:18px 20px;border-right:1px solid var(--border-dim)}
.detail-col:last-child{border-right:none}
.d-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--accent-dim);margin-bottom:8px}
.d-text{font-size:12px;color:var(--text-2);line-height:1.6}
.d-next{font-size:12px;color:var(--accent);line-height:1.6}
.d-blocker{font-size:12px;color:#dc2626;font-weight:600;line-height:1.6}
.d-section{margin-bottom:16px}
.d-section:last-child{margin-bottom:0}

/* Links in detail */
.link-chips{display:flex;gap:8px;flex-wrap:wrap}
.link-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;border-radius:8px;border:1px solid var(--border);background:#fafaff;font-size:12px;font-weight:500;color:var(--accent);text-decoration:none;transition:all .12s}
.link-chip:hover{background:var(--accent-bg);border-color:var(--accent-dim);text-decoration:none}
.link-chip svg{width:13px;height:13px;flex-shrink:0}

/* Field notes in detail */
.fn-entry{margin-bottom:10px;padding-bottom:10px;border-bottom:1px dashed var(--border-dim)}
.fn-entry:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.fn-date{font-size:11px;font-weight:700;color:var(--accent);margin-bottom:3px}
.fn-preview{font-size:11px;color:var(--text-3);line-height:1.5;cursor:pointer}
.fn-preview:hover{color:var(--text-2)}
.fn-body{font-size:11px;color:var(--text-2);line-height:1.6}
.fn-body p{margin-bottom:6px}
.fn-body p:last-child{margin-bottom:0}

/* Timeline in detail */
.timeline-full{position:relative;padding-left:18px}
.timeline-full::before{content:'';position:absolute;left:5px;top:6px;bottom:6px;width:1px;background:var(--border)}
.timeline-entry{position:relative;padding:3px 0 3px 12px;font-size:11px}
.timeline-entry::before{content:'';position:absolute;left:-1px;top:8px;width:9px;height:9px;border-radius:50%;background:var(--surface);border:2px solid var(--border)}
.timeline-entry.milestone::before{background:var(--accent);border-color:var(--accent)}
.timeline-date{color:var(--accent);font-weight:600;margin-right:8px}
.timeline-event{color:var(--text-2)}
.timeline-entry.milestone .timeline-event{color:var(--text);font-weight:600}
.timeline-loading{color:var(--text-3);font-size:11px;padding:4px 0 4px 12px}
.timeline-scroll{max-height:260px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:var(--border) var(--bg)}
.timeline-scroll::-webkit-scrollbar{width:4px}
.timeline-scroll::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.timeline-show-more{color:var(--accent);font-size:11px;cursor:pointer;padding:6px 0 2px;user-select:none;font-weight:600}
.timeline-show-more:hover{text-decoration:underline}

/* SKELETON */
.skeleton-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow-sm)}
.skeleton-img{width:100%;height:90px;background:var(--border);animation:pulse 1.5s ease-in-out infinite}
.skeleton-body{padding:12px 14px}
.skeleton-bar{height:11px;background:var(--border);border-radius:4px;margin-bottom:8px;animation:pulse 1.5s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.4}50%{opacity:.8}}
.skel-id{width:40px}.skel-name{width:120px}.skel-summary{width:90%;margin-top:4px}

/* HELP OVERLAY */
.help-overlay{display:none;position:fixed;inset:0;background:rgba(30,27,75,.7);z-index:200;align-items:center;justify-content:center}
.help-overlay.show{display:flex}
.help-box{background:var(--surface);border:1px solid var(--border);padding:24px 32px;max-width:400px;border-radius:14px;box-shadow:var(--shadow-md)}
.help-box h2{color:var(--accent);font-size:14px;margin-bottom:16px;letter-spacing:.05em;text-transform:uppercase}
.help-row{display:flex;justify-content:space-between;padding:5px 0;font-size:12px;border-bottom:1px solid var(--border-dim)}
.help-row:last-of-type{border-bottom:none}
.help-key{color:var(--accent);font-weight:700;min-width:60px;font-family:'Courier New',monospace}
.help-desc{color:var(--text-2)}
.help-close{color:var(--text-3);font-size:11px;text-align:center;margin-top:14px;cursor:pointer}

/* JOURNAL (right side) */
.journal{flex:0 0 var(--panel-w);background:var(--surface);border:1px solid var(--border);border-radius:14px;position:sticky;top:24px;height:calc(100vh - 48px);overflow-y:auto;display:flex;flex-direction:column;box-shadow:var(--shadow-sm);transition:flex-basis .25s ease}
.journal.collapsed{flex-basis:var(--rail-w)}
.journal.collapsed .journal-body,.journal.collapsed .journal-head .journal-tabs,.journal.collapsed .journal-head .journal-title{display:none}
.journal-head{padding:14px 16px 8px;border-bottom:1px solid var(--border-dim);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.journal-title{color:var(--text);font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;flex:1}
.journal-toggle{background:none;border:1px solid var(--border);color:var(--accent);font-family:var(--font);font-size:11px;padding:2px 7px;cursor:pointer;border-radius:6px}
.journal-toggle:hover{background:var(--accent-bg)}
.journal-stale-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#d97706;margin-left:4px}
.journal-tabs{display:flex;gap:4px;width:100%}
.journal-tab{padding:4px 10px;font-size:11px;border:1px solid var(--border);color:var(--text-3);background:#fafaff;border-radius:6px;text-decoration:none;text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.journal-tab.active{color:var(--accent);border-color:var(--accent);background:var(--accent-bg)}
.journal-tab:hover{color:var(--text-2);text-decoration:none}
.journal-body{padding:8px 14px 24px;flex:1}
.journal-empty{color:var(--text-3);font-size:11px;padding:14px 0}
.journal-entry{padding:12px 0;border-bottom:1px dashed var(--border-dim)}
.journal-entry:last-child{border-bottom:0}
.journal-entry-date{color:var(--accent);font-size:11px;font-weight:700;letter-spacing:.04em;margin-bottom:5px}
.journal-entry-meta{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:7px}
.rep-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--accent);background:var(--accent-bg);border:1px solid var(--border);border-radius:4px;cursor:pointer;font-family:var(--font)}
.rep-chip:hover{border-color:var(--accent)}
.tag-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--text-3);background:transparent;border:1px solid var(--border);border-radius:4px}
.journal-entry-body{color:var(--text-2);font-size:12px;line-height:1.55}
.journal-entry-body p{margin-bottom:7px}
.journal-entry-body p:last-child{margin-bottom:0}
.journal-entry-preview{color:var(--text-3);font-size:12px;line-height:1.5;cursor:pointer}
.journal-entry-preview:hover{color:var(--text-2)}
.journal-entry .wl-rep{color:var(--accent);font-weight:700;text-decoration:none;border-bottom:1px dotted var(--accent)}
.journal-entry .wl-lesson{color:#7e22ce;text-decoration:none;border-bottom:1px dotted #7e22ce}
.journal-rail{display:none;writing-mode:vertical-rl;transform:rotate(180deg);color:var(--text-3);font-size:10px;letter-spacing:3px;padding:14px 0;cursor:pointer;user-select:none;text-transform:uppercase}
.journal.collapsed .journal-rail{display:block;text-align:center;width:var(--rail-w)}
.journal.collapsed .journal-head{display:none}

/* MOBILE */
@media(max-width:1023px){
  .card-grid{grid-template-columns:repeat(2,1fr)}
  .detail-body{grid-template-columns:1fr}
  .detail-col{border-right:none;border-bottom:1px solid var(--border-dim)}
  .detail-col:last-child{border-bottom:none}
}
@media(max-width:900px){
  .app-shell{display:block}
  .journal{position:fixed;top:0;right:0;height:100vh;z-index:50;flex-basis:var(--rail-w);width:var(--rail-w);border-radius:0;border-right:none;border-left:1px solid var(--border)}
  .journal:not(.collapsed){width:min(340px,90vw);flex-basis:auto}
  .journal.collapsed .journal-rail{display:block;height:100vh}
  .grid-col{margin-right:calc(var(--rail-w) + 20px)}
}
@media(max-width:639px){
  .card-grid{grid-template-columns:1fr}
  .header{padding:16px 16px 0}
  .filter-row{padding:12px 16px}
  .app-shell{padding:0 16px 60px}
  .progress-track{width:140px}
  .search-input{width:120px}
}
</style>
```

- [ ] **Step 4: Verify page loads without JS errors**

```bash
npm run dev
```

Open http://localhost:3000/index-v2.html — the page should load. Layout will look wrong (table still renders) but the browser console should show zero errors.

- [ ] **Step 5: Commit**

```bash
git add docs/index-v2.html
git commit -m "feat(redesign): bootstrap index-v2.html with light theme CSS"
```

---

## Task 2: Rewrite HTML shell structure

**Files:**
- Modify: `docs/index-v2.html`

Replace the `<body>` HTML (keep all `<script>` content identical). The new shell moves the journal to the right, drops the table + cards-view, and uses `.card-grid` as the primary rep container.

- [ ] **Step 1: Replace the full `<body>` HTML (above the `<script>` tag)**

Find the `<body>` opening tag down to (but not including) the `<script src="...js-yaml...">` line and replace with:

```html
<body>

<div class="error-banner" id="errorBanner"></div>

<div class="header">
  <div class="header-top">
    <div>
      <div class="brand-title">100 Reps Project</div>
      <div class="header-sub"><a href="https://100reps.substack.com/" target="_blank" rel="noopener">One guy, 100 AI-powered businesses &mdash; can a solo founder with AI actually build something massive?</a></div>
    </div>
    <div class="progress-area">
      <div class="progress-label" id="countLabel">0/100</div>
      <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
    </div>
  </div>
  <div class="last-updated">Updated: <span id="lastUpdated"></span> <span class="feed-flash" id="feedFlash">FEED UPDATED</span></div>
</div>

<div class="filter-row" id="filterRow">
  <div id="statusCounts" style="display:contents"></div>
  <div class="search-wrap">
    <label>Search</label>
    <input type="text" id="searchInput" class="search-input" placeholder="Filter reps…" autocomplete="off">
  </div>
</div>

<div class="app-shell">

  <div class="grid-col">
    <div class="card-grid" id="cardGrid">
      <!-- skeleton cards shown while loading -->
      <div class="skeleton-card"><div class="skeleton-img"></div><div class="skeleton-body"><div class="skeleton-bar skel-id"></div><div class="skeleton-bar skel-name"></div><div class="skeleton-bar skel-summary"></div></div></div>
      <div class="skeleton-card"><div class="skeleton-img"></div><div class="skeleton-body"><div class="skeleton-bar skel-id"></div><div class="skeleton-bar skel-name"></div><div class="skeleton-bar skel-summary"></div></div></div>
      <div class="skeleton-card"><div class="skeleton-img"></div><div class="skeleton-body"><div class="skeleton-bar skel-id"></div><div class="skeleton-bar skel-name"></div><div class="skeleton-bar skel-summary"></div></div></div>
    </div>
  </div>

  <aside class="journal" id="journalPanel">
    <div class="journal-rail" id="journalRail">FIELD&nbsp;NOTES</div>
    <div class="journal-head">
      <div class="journal-title">Field Notes <span id="journalStaleDot" class="journal-stale-dot" style="display:none" title="No entry in &gt;3 days"></span></div>
      <button class="journal-toggle" id="journalToggle" title="Collapse panel">&laquo;</button>
      <div class="journal-tabs">
        <a class="journal-tab active" href="#">Notes</a>
        <a class="journal-tab" href="lessons.html">Lessons &rarr;</a>
      </div>
    </div>
    <div class="journal-body" id="journalBody">
      <div class="journal-empty">Loading&hellip;</div>
    </div>
  </aside>

</div>

<div class="help-overlay" id="helpOverlay">
  <div class="help-box">
    <h2>Keyboard Shortcuts</h2>
    <div class="help-row"><span class="help-key">j / k</span><span class="help-desc">Move selection down / up</span></div>
    <div class="help-row"><span class="help-key">Enter</span><span class="help-desc">Expand / collapse selected card</span></div>
    <div class="help-row"><span class="help-key">Esc</span><span class="help-desc">Collapse all / close help</span></div>
    <div class="help-row"><span class="help-key">/</span><span class="help-desc">Focus search</span></div>
    <div class="help-row"><span class="help-key">?</span><span class="help-desc">Toggle this help</span></div>
    <div class="help-row"><span class="help-key">1-6</span><span class="help-desc">Filter by status</span></div>
    <div class="help-row"><span class="help-key">0</span><span class="help-desc">Show all</span></div>
    <div class="help-close" onclick="document.getElementById('helpOverlay').classList.remove('show')">Click or press Esc to close</div>
  </div>
</div>

<noscript>
  <div style="padding:40px;color:#dc2626;text-align:center;font-family:sans-serif">
    JavaScript is required to load the 100 Reps dashboard.
  </div>
</noscript>
```

- [ ] **Step 2: Update the progress bar DOM ref in JS**

In the `<script>` block, find:
```javascript
var $progressBar = document.getElementById('progressBar');
```
Replace with:
```javascript
var $progressFill = document.getElementById('progressFill');
```

Find the `renderHeader()` function. Find the lines that build `barHtml` and set `$progressBar.innerHTML = barHtml`. Replace the entire progress bar rendering block:

Old (the `barHtml` loop + `$progressBar.innerHTML` assignment):
```javascript
  // Segmented progress bar
  var barHtml = '';
  STATUS_ORDER.forEach(function(s) {
    if (counts[s] > 0) {
      var pct = ((counts[s] / target) * 100).toFixed(1);
      barHtml += '<div class="seg" style="width:'+pct+'%;background:'+STATUS_COLORS[s]+'" title="'+s+': '+counts[s]+'"></div>';
    }
  });
  var filled = 0;
  STATUS_ORDER.forEach(function(s) { filled += counts[s]; });
  var emptyPct = (((target - filled) / target) * 100).toFixed(1);
  barHtml += '<div class="seg" style="width:'+emptyPct+'%;background:var(--bg3)"></div>';
  $progressBar.innerHTML = barHtml;
```

New:
```javascript
  // Single fill bar showing overall progress
  var filled = 0;
  STATUS_ORDER.forEach(function(s) { filled += counts[s]; });
  var fillPct = ((filled / target) * 100).toFixed(1);
  if ($progressFill) $progressFill.style.width = fillPct + '%';
```

- [ ] **Step 3: Remove old DOM refs that no longer exist**

Find and delete these variable declarations near the top of the `<script>`:
```javascript
var $body = document.getElementById('tableBody');
```
(We will add `var $cardGrid = document.getElementById('cardGrid');` in Task 3.)

Also delete:
```javascript
var $filterBtns = null;
var $clearFilter = null;
```
```javascript
var $tableWrap = document.getElementById('tableWrap');
var $cardsView = document.getElementById('cardsView');
var $viewToggle = document.getElementById('viewToggle');
```
```javascript
var viewMode = 'table';
```

And delete the view-toggle event listener:
```javascript
$viewToggle.addEventListener('click', toggleViewMode);
```

And delete the `toggleViewMode` function entirely:
```javascript
function toggleViewMode() {
  viewMode = viewMode === 'table' ? 'cards' : 'table';
  $viewToggle.textContent = viewMode === 'table' ? 'CARDS' : 'TABLE';
  $tableWrap.className = 'table-wrap ' + (viewMode === 'table' ? 'table-active' : 'cards-active');
  $cardsView.className = 'cards-view ' + (viewMode === 'table' ? 'table-active' : 'cards-active');
}
```

And delete the column header sort binding block (no table headers exist anymore):
```javascript
/* ── Column header sort binding ── */
document.querySelectorAll('thead th[data-col]').forEach(function(th) {
  th.addEventListener('click', function() { setSort(th.dataset.col); });
});
```

- [ ] **Step 4: Verify in browser**

Reload http://localhost:3000/index-v2.html — the skeleton cards should show, journal panel should be on the right, no console errors. Data won't render yet (renderTable will fail silently since `#tableBody` is gone).

- [ ] **Step 5: Commit**

```bash
git add docs/index-v2.html
git commit -m "feat(redesign): rewrite HTML shell — card grid + right-side journal"
```

---

## Task 3: Implement renderCardGrid() — cards with letter avatars

**Files:**
- Modify: `docs/index-v2.html`

Replace the table-rendering JS with the card grid renderer. No images yet — all cards use letter avatars. Verifies that filtering, sorting, search, and keyboard nav all work.

- [ ] **Step 1: Add cardGrid DOM ref and change expandedIds to expandedId**

At the top of the `<script>` block, find:
```javascript
var expandedIds = {};
```
Replace with:
```javascript
var expandedId = null;
```

Add after the existing DOM refs block:
```javascript
var $cardGrid = document.getElementById('cardGrid');
```

- [ ] **Step 2: Replace renderTable() and renderCards() with renderCardGrid()**

Delete the entire `renderTable(filtered)` function (from its opening line to its closing `}`).

Delete the entire `renderCards(filtered)` function.

In their place, add the following new functions. Insert them before the `render()` function:

```javascript
/* ── Avatar color helper ── */
var AVATAR_GRADIENT = {
  idea:'linear-gradient(135deg,#4f46e5,#a5b4fc)',
  assessed:'linear-gradient(135deg,#6b7280,#9ca3af)',
  building:'linear-gradient(135deg,#d97706,#fbbf24)',
  live:'linear-gradient(135deg,#059669,#34d399)',
  pmf:'linear-gradient(135deg,#7e22ce,#c084fc)',
  dead:'linear-gradient(135deg,#9ca3af,#d1d5db)'
};

function buildCardHtml(rep, idx) {
  var isDead = rep.status === 'dead';
  var staleDays = daysSince(rep.last_action);
  var isSelected = rep.id === expandedId;
  var isSelectedIdx = selectedIdx === idx;

  var cardClass = 'rep-card' +
    (isDead ? ' dead-card' : '') +
    (isSelected ? ' selected' : '') +
    (isSelectedIdx && !isSelected ? ' selected' : '');

  var safeNext = sanitizeNextStep(rep.next_step);
  var staleHtml = (!isDead && staleDays > 14)
    ? '<span class="rc-stale">' + staleDays + 'd</span>'
    : '';

  // Image area: placeholder for now (Task 4 adds real images)
  var imgHtml = '<div class="rc-avatar av-' + rep.status + '">' +
    esc(rep.name.charAt(0).toUpperCase()) + '</div>';

  var nextHtml = safeNext
    ? '<div class="rc-next"><span style="flex-shrink:0;opacity:.6">&#8594;</span> ' + truncate(safeNext, 60) + '</div>'
    : '';

  return '<div class="' + cardClass + '" data-id="' + rep.id + '" data-idx="' + idx + '">' +
    imgHtml +
    '<div class="rc-body">' +
      '<div class="rc-meta">' +
        '<span class="rc-id">Rep ' + String(rep.id).padStart(3,'0') + '</span>' +
        '<span class="rc-tag tag-' + rep.status + '">' +
          STATUS_ICONS[rep.status] + ' ' + rep.status + '</span>' +
      '</div>' +
      '<div class="rc-name">' + esc(rep.name) + staleHtml + '</div>' +
      '<div class="rc-summary">' + truncate(rep.summary, 80) + '</div>' +
      nextHtml +
    '</div>' +
  '</div>';
}

function renderCardGrid(filtered) {
  var cols = window.innerWidth >= 1024 ? 3 : window.innerWidth >= 640 ? 2 : 1;
  var html = '';
  filtered.forEach(function(rep, idx) {
    html += buildCardHtml(rep, idx);
    var isLastInRow = (idx % cols === cols - 1) || (idx === filtered.length - 1);
    if (isLastInRow && expandedId !== null) {
      var rowStart = idx - (idx % cols);
      var inThisRow = filtered.slice(rowStart, idx + 1).some(function(r) {
        return r.id === expandedId;
      });
      if (inThisRow) {
        var expandedRep = filtered.filter(function(r) { return r.id === expandedId; })[0];
        if (expandedRep) html += buildDetailExpander(expandedRep);
      }
    }
  });
  $cardGrid.innerHTML = html;

  // Bind card click events
  $cardGrid.querySelectorAll('.rep-card').forEach(function(card) {
    card.addEventListener('click', function(e) {
      if (e.target.closest('a') || e.target.closest('.timeline-show-more') ||
          e.target.closest('.dh-close')) return;
      var id = parseInt(card.dataset.id);
      var idx = parseInt(card.dataset.idx);
      toggleExpand(id, idx);
    });
  });

  // Wire close button in expander
  var closeBtn = $cardGrid.querySelector('.dh-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      expandedId = null;
      render();
    });
  }

  // Load timeline for expanded rep
  if (expandedId !== null) {
    var expandedRep2 = filtered.filter(function(r) { return r.id === expandedId; })[0];
    if (expandedRep2) loadTimeline(expandedRep2);
  }
}

/* Placeholder — replaced in Task 5 */
function buildDetailExpander(rep) {
  return '<div class="detail-bridge">' +
    '<div class="detail-header">' +
      '<div class="dh-thumb-av av-' + rep.status + '">' + esc(rep.name.charAt(0).toUpperCase()) + '</div>' +
      '<div><div class="dh-name">' + esc(rep.name) + '</div>' +
        '<div class="dh-meta">Rep ' + String(rep.id).padStart(3,'0') +
          (rep.pita ? ' &middot; PITA ' + rep.pita : '') +
          (rep.last_action ? ' &middot; Last: ' + esc(formatDate(rep.last_action)) : '') +
        '</div></div>' +
      '<span class="rc-tag tag-' + rep.status + ' dh-tag">' + STATUS_ICONS[rep.status] + ' ' + rep.status + '</span>' +
      '<button class="dh-close" title="Close">&times;</button>' +
    '</div>' +
    '<div style="padding:16px 20px;color:var(--text-3);font-size:12px">Detail panel coming in Task 5&hellip;</div>' +
  '</div>';
}
```

- [ ] **Step 3: Update render() to call renderCardGrid**

Find the `render()` function:
```javascript
function render() {
  var filtered = getFilteredSorted();
  renderHeader();
  renderTable(filtered);
  renderCards(filtered);
  updateTimestamp();
}
```

Replace with:
```javascript
function render() {
  var filtered = getFilteredSorted();
  renderHeader();
  renderCardGrid(filtered);
  updateTimestamp();
}
```

- [ ] **Step 4: Update toggleExpand() to use expandedId**

Find the `toggleExpand(id, idx)` function and replace it:

```javascript
function toggleExpand(id, idx) {
  expandedId = (expandedId === id) ? null : id;
  if (idx !== undefined) selectedIdx = idx;
  render();
}
```

- [ ] **Step 5: Update scrollToRep() to scroll to card element**

Find `scrollToRep(id)` and replace:

```javascript
function scrollToRep(id) {
  expandedId = id;
  render();
  var card = $cardGrid.querySelector('.rep-card[data-id="' + id + '"]');
  if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
```

- [ ] **Step 6: Update keyboard nav — Escape key**

Find the `case 'Escape':` block. Update the last else branch to use `expandedId`:

```javascript
    case 'Escape':
      if ($helpOverlay.classList.contains('show')) {
        $helpOverlay.classList.remove('show');
      } else if (document.activeElement === $search) {
        $search.blur();
        searchTerm = '';
        $search.value = '';
        render();
      } else {
        expandedId = null;
        selectedIdx = -1;
        render();
      }
      break;
```

- [ ] **Step 7: Verify**

Reload http://localhost:3000/index-v2.html. Verify:
- All reps render as cards with letter avatars
- Filter pills (click status names) correctly filter cards
- Search box filters by name/summary
- `j`/`k` moves selection highlight between cards
- `Enter` expands a card showing the placeholder detail panel
- `Esc` collapses the expander

- [ ] **Step 8: Commit**

```bash
git add docs/index-v2.html
git commit -m "feat(redesign): implement renderCardGrid with letter avatars"
```

---

## Task 4: Implement fetchRepImage() — logo lookup and caching

**Files:**
- Modify: `docs/index-v2.html`

Adds image loading to cards. Each card tries: (1) `rep.image` field, (2) common logo paths in the GitHub repo via raw.githubusercontent.com, (3) letter avatar. Uses `<img onerror>` chaining — no extra fetch calls needed.

- [ ] **Step 1: Add imageCache state variable**

Near the top of the `<script>` block, after `var gitCommitCache = {};`, add:

```javascript
var imageCache = {}; // keyed by rep id: url string | null (null = use avatar)
```

- [ ] **Step 2: Add the global image-error handler before the IIFE**

Add these lines immediately before the `<script>` block's IIFE opening `(function(){`:

```javascript
// Global handlers for image fallback chain (called from onerror/onload attributes)
window.__imgNext = function(repId, idx, imgEl, status, initial) {
  var candidates = window.__imgCandidates && window.__imgCandidates[repId];
  if (!candidates) { window.__imgFallback(repId, imgEl, status, initial); return; }
  if (idx >= candidates.length) { window.__imgFallback(repId, imgEl, status, initial); return; }
  imgEl.src = candidates[idx];
  imgEl.onerror = function() { window.__imgNext(repId, idx + 1, imgEl, status, initial); };
};
window.__imgFallback = function(repId, imgEl, status, initial) {
  if (window.__imgCache) window.__imgCache[repId] = null;
  imgEl.outerHTML = '<div class="rc-avatar av-' + status + '">' + initial + '</div>';
};
window.__imgDone = function(repId, src) {
  if (window.__imgCache) window.__imgCache[repId] = src;
};
```

- [ ] **Step 3: Add buildImageHtml() and wire the cache inside the IIFE**

Inside the IIFE, after `var imageCache = {};` add:

```javascript
window.__imgCache = imageCache;
window.__imgCandidates = {}; // keyed by rep id: array of URL strings to try
var LOGO_PATHS = ['logo.png','logo.svg','logo.jpg','public/logo.png','assets/logo.png'];

function buildImageHtml(rep) {
  var initial = esc(rep.name.charAt(0).toUpperCase());
  var avatarHtml = '<div class="rc-avatar av-' + rep.status + '">' + initial + '</div>';

  // Already resolved
  if (imageCache[rep.id] === null) return avatarHtml;
  if (imageCache[rep.id]) {
    return '<img class="rc-image" src="' + esc(imageCache[rep.id]) + '" alt="" ' +
      'onerror="window.__imgFallback(' + rep.id + ',this,\'' + rep.status + '\',\'' + initial + '\')">';
  }

  // No image field and no repo → avatar immediately
  if (!rep.image && !rep.repo) {
    imageCache[rep.id] = null;
    return avatarHtml;
  }

  // Build candidate list and store globally for the onerror handler
  var candidates = rep.image ? [rep.image] :
    LOGO_PATHS.map(function(p) {
      return 'https://raw.githubusercontent.com/' + rep.repo + '/HEAD/' + p;
    });
  window.__imgCandidates[rep.id] = candidates.slice(1); // handler gets called with idx=0 on first error

  return '<img class="rc-image" src="' + esc(candidates[0]) + '" alt="" ' +
    'onerror="window.__imgNext(' + rep.id + ',0,this,\'' + rep.status + '\',\'' + initial + '\')" ' +
    'onload="window.__imgDone(' + rep.id + ',this.src)">';
}
```

- [ ] **Step 4: Update buildCardHtml() to use buildImageHtml()**

In `buildCardHtml(rep, idx)`, replace:
```javascript
  var imgHtml = '<div class="rc-avatar av-' + rep.status + '">' +
    esc(rep.name.charAt(0).toUpperCase()) + '</div>';
```
With:
```javascript
  var imgHtml = buildImageHtml(rep);
```

- [ ] **Step 5: Verify**

Reload http://localhost:3000/index-v2.html. Reps with a `repo` value (most have one) will attempt to load `logo.png` from raw.githubusercontent.com. Most will 404 and fall back to the letter avatar gracefully. Check browser Network tab — 404s on logo files are expected; verify no JS errors appear.

- [ ] **Step 6: Commit**

```bash
git add docs/index-v2.html
git commit -m "feat(redesign): add fetchRepImage with onerror fallback chain"
```

---

## Task 5: Implement buildDetailExpander() — full detail panel

**Files:**
- Modify: `docs/index-v2.html`

Replaces the placeholder `buildDetailExpander` from Task 3 with the full 2-column panel: summary / next step / blocker / links (left) + field notes / timeline (right).

- [ ] **Step 1: Replace the placeholder buildDetailExpander() with the full implementation**

Find and replace the entire placeholder function:

```javascript
function buildDetailExpander(rep) {
  var safeNext = sanitizeNextStep(rep.next_step);
  var repNotes = fieldNotesForRep(rep.id);

  // Thumb: cached image or avatar
  var thumbHtml = imageCache[rep.id]
    ? '<img class="dh-thumb" src="' + esc(imageCache[rep.id]) + '" alt="">'
    : '<div class="dh-thumb-av av-' + rep.status + '">' +
        esc(rep.name.charAt(0).toUpperCase()) + '</div>';

  // Left column: summary, blocker, next step, links
  var leftHtml = '';

  leftHtml += '<div class="d-section"><div class="d-label">Summary</div>' +
    '<div class="d-text">' + esc(rep.summary) + '</div></div>';

  if (rep.blocker) {
    leftHtml += '<div class="d-section"><div class="d-label">Blocker</div>' +
      '<div class="d-blocker">' + esc(rep.blocker) + '</div></div>';
  }

  if (safeNext) {
    leftHtml += '<div class="d-section"><div class="d-label">Next Step</div>' +
      '<div class="d-next">&#8594; ' + esc(safeNext) + '</div></div>';
  }

  var linkEntries = buildLinkEntries(rep);
  if (linkEntries.length > 0) {
    leftHtml += '<div class="d-section"><div class="d-label">Links</div>' +
      '<div class="link-chips">';
    linkEntries.forEach(function(l) {
      leftHtml += '<a class="link-chip" href="' + esc(l.url) + '" target="_blank" rel="noopener">' +
        l.svg + ' ' + esc(l.short) + '</a>';
    });
    leftHtml += '</div></div>';
  }

  // Right column: field notes, timeline
  var rightHtml = '';

  if (repNotes.length > 0) {
    rightHtml += '<div class="d-section"><div class="d-label">Field Notes (' + repNotes.length + ')</div>';
    repNotes.slice(0, 5).forEach(function(en) {
      rightHtml += '<div class="fn-entry">' +
        '<div class="fn-date">' + esc(en.date) + '</div>' +
        '<div class="fn-preview" data-fn-date="' + esc(en.date) + '">' +
          esc(en.preview || '') + '</div>' +
      '</div>';
    });
    if (repNotes.length > 5) {
      rightHtml += '<div style="color:var(--text-3);font-size:11px">+ ' +
        (repNotes.length - 5) + ' older entries</div>';
    }
    rightHtml += '</div>';
  }

  var timelineContainerId = 'tl-' + rep.id;
  rightHtml += '<div class="d-section"><div class="d-label">Timeline</div>' +
    '<div class="timeline-full" id="' + timelineContainerId + '">' +
      '<div class="timeline-loading">Loading history&hellip;</div>' +
    '</div></div>';

  return '<div class="detail-bridge" data-expander="' + rep.id + '">' +
    '<div class="detail-header">' +
      thumbHtml +
      '<div>' +
        '<div class="dh-name">' + esc(rep.name) + '</div>' +
        '<div class="dh-meta">Rep ' + String(rep.id).padStart(3,'0') +
          (rep.pita ? ' &middot; PITA ' + rep.pita : '') +
          (rep.last_action ? ' &middot; Last action: ' + esc(formatDate(rep.last_action)) : '') +
        '</div>' +
      '</div>' +
      '<span class="rc-tag tag-' + rep.status + ' dh-tag">' +
        STATUS_ICONS[rep.status] + ' ' + rep.status + '</span>' +
      '<button class="dh-close" title="Close">&times;</button>' +
    '</div>' +
    '<div class="detail-body">' +
      '<div class="detail-col">' + leftHtml + '</div>' +
      '<div class="detail-col">' + rightHtml + '</div>' +
    '</div>' +
  '</div>';
}
```

- [ ] **Step 2: Update loadTimeline() to target the new container ID**

The existing `loadTimeline(rep)` function looks for `document.getElementById('timeline-' + rep.id)` and `document.getElementById('card-timeline-' + rep.id)`. Update it to also check the new expander container:

Find `loadTimeline(rep)`:
```javascript
function loadTimeline(rep) {
  fetchGitHistory(rep).then(function(gitCommits) {
    var merged = mergeTimelines(rep.timeline, gitCommits);
    var containers = [
      document.getElementById('timeline-' + rep.id),
      document.getElementById('card-timeline-' + rep.id)
    ];
    containers.forEach(function(el) {
      if (el) renderTimelineEntries(el, merged, rep.id);
    });
  });
}
```

Replace with:
```javascript
function loadTimeline(rep) {
  fetchGitHistory(rep).then(function(gitCommits) {
    var merged = mergeTimelines(rep.timeline, gitCommits);
    var el = document.getElementById('tl-' + rep.id);
    if (el) renderTimelineEntries(el, merged, rep.id);
  });
}
```

- [ ] **Step 3: Wire field-note expand-on-click in detail panel**

In `renderCardGrid()`, after binding the close button event, add:

```javascript
  // Expand field note previews on click within the detail panel
  $cardGrid.querySelectorAll('.fn-preview').forEach(function(el) {
    el.addEventListener('click', function() {
      var date = el.dataset.fnDate;
      var entry = fieldNotes.filter(function(e) { return e.date === date; })[0];
      if (!entry) return;
      var $body = document.createElement('div');
      $body.className = 'fn-body';
      $body.innerHTML = entry.html; // sanitized server-side
      $body.querySelectorAll('a.wl-rep').forEach(function(a) {
        a.addEventListener('click', function(ev) {
          ev.preventDefault();
          var rid = parseInt(a.dataset.repId);
          if (!isNaN(rid)) scrollToRep(rid);
        });
      });
      el.parentNode.replaceChild($body, el);
    });
  });
```

- [ ] **Step 4: Verify**

Reload http://localhost:3000/index-v2.html. Click any card with a repo:
- Detail expander appears below the card's row spanning full width
- Summary, next step, links all show correctly
- Timeline loads git commits after a moment
- Field notes count shows if the rep has journal entries
- Clicking a field note preview expands to full body
- Close (✕) button collapses the expander
- Clicking a different card switches the expander to that card

- [ ] **Step 5: Commit**

```bash
git add docs/index-v2.html
git commit -m "feat(redesign): implement full detail expander with timeline and field notes"
```

---

## Task 6: Wire renderHeader() for new filter pill layout

**Files:**
- Modify: `docs/index-v2.html`

The current `renderHeader()` renders pills into `#statusCounts` and also manages a separate filter-buttons div that no longer exists. Simplify it to generate only the pill row.

- [ ] **Step 1: Replace renderHeader()**

Find the entire `renderHeader()` function and replace it:

```javascript
function renderHeader() {
  var total = meta.total || reps.length;
  var target = meta.target || 100;
  $countLabel.textContent = total + '/' + target;

  var counts = {};
  STATUS_ORDER.forEach(function(s) { counts[s] = 0; });
  reps.forEach(function(r) { if (counts[r.status] !== undefined) counts[r.status]++; });

  // Progress fill
  var filled = 0;
  STATUS_ORDER.forEach(function(s) { filled += counts[s]; });
  if ($progressFill) $progressFill.style.width = ((filled / target) * 100).toFixed(1) + '%';

  // Filter pills
  var STATUS_PILL_COLORS = {
    idea:'#ede9fe|#6d28d9', assessed:'#f3f4f6|#374151',
    building:'#fef9c3|#92400e', live:'#d1fae5|#065f46',
    pmf:'#fae8ff|#7e22ce', dead:'#f3f4f6|#9ca3af'
  };
  var pillsHtml = '';
  var allActive = currentFilter === 'all';
  pillsHtml += '<button class="filter-pill' + (allActive ? ' active' : '') + '" data-status="all">' +
    'All ' + total + '</button>';
  STATUS_ORDER.forEach(function(s) {
    if (counts[s] === 0) return;
    var isActive = currentFilter === s;
    var colors = (STATUS_PILL_COLORS[s] || '#f3f4f6|#374151').split('|');
    var style = isActive ? '' :
      'background:' + colors[0] + ';color:' + colors[1];
    pillsHtml += '<button class="filter-pill' + (isActive ? ' active' : '') + '" ' +
      'style="' + style + '" data-status="' + s + '">' +
      STATUS_ICONS[s] + ' ' + s.charAt(0).toUpperCase() + s.slice(1) + ' ' + counts[s] +
      '</button>';
  });
  $counts.innerHTML = pillsHtml;
  $counts.querySelectorAll('.filter-pill').forEach(function(el) {
    el.addEventListener('click', function() { setFilter(el.dataset.status); });
  });
}
```

- [ ] **Step 2: Verify**

Reload. Filter pills across the top should show "All 20", "✓ Live 3", etc. Clicking each filters the card grid. The search box remains right-aligned in the same row.

- [ ] **Step 3: Commit**

```bash
git add docs/index-v2.html
git commit -m "feat(redesign): simplify renderHeader for pill-only filter row"
```

---

## Task 7: Verify journal chrome and scrollToRep

**Files:**
- Modify: `docs/index-v2.html`

The journal sidebar HTML IDs match what `wireJournalChrome()` and `renderJournal()` expect, so no code changes are needed — just verification. This task confirms the journal panel works correctly in the new layout.

- [ ] **Step 1: Check wireJournalChrome() IDs match the new HTML**

Confirm these IDs exist in the new HTML shell (from Task 2): `journalPanel`, `journalToggle`, `journalRail`, `journalBody`, `journalStaleDot`. They do — no code change needed.

- [ ] **Step 2: Verify journal functionality**

Open http://localhost:3000/index-v2.html and verify:
- Field notes entries appear in the right-side sidebar
- Clicking `«` collapses the panel to a rail; clicking the rail re-expands it
- Collapse state persists after page refresh (localStorage)
- Clicking a rep chip (e.g., `002`) in a journal entry scrolls the grid to that card
- Stale dot appears in journal title if no entry in >3 days

- [ ] **Step 3: Verify keyboard navigation with cards**

- Press `j` / `k` — selection highlight moves between cards
- Press `Enter` on a selected card — detail expander opens
- Press `Esc` — expander closes
- Press `?` — help overlay appears with new copy

- [ ] **Step 4: Commit (no code changes needed — commit verification notes only if desired)**

If no changes were required, nothing to commit. If any small fixes were needed, commit them:
```bash
git add docs/index-v2.html
git commit -m "fix(redesign): journal chrome and keyboard nav corrections"
```

---

## Task 8: Update lessons.html to light theme

**Files:**
- Modify: `docs/lessons.html`

CSS token swap and font change only. No HTML or JS changes.

- [ ] **Step 1: Replace the font link in lessons.html**

Old:
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```
New:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

- [ ] **Step 2: Replace the entire `<style>` block in lessons.html**

```html
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f5f5ff;--surface:#fff;--border:#e0e7ff;--border-dim:#f0f0ff;
  --accent:#4f46e5;--accent-dim:#a5b4fc;--accent-bg:#ede9fe;
  --text:#1e1b4b;--text-2:#374151;--text-3:#6b7280;
  --font:'Inter',system-ui,sans-serif;
}
html,body{background:var(--bg);color:var(--text);font-family:var(--font);font-size:13px;line-height:1.5;min-height:100vh}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:760px;margin:0 auto;padding:32px 24px 80px}
.crumb{font-size:11px;color:var(--text-3);letter-spacing:.1em;margin-bottom:8px;text-transform:uppercase}
.crumb a{color:var(--accent)}
h1{color:var(--text);font-size:22px;font-weight:800;letter-spacing:-.3px;margin-bottom:6px}
.sub{color:var(--text-3);font-size:12px;margin-bottom:32px}
.lesson{padding:24px 0;border-bottom:1px solid var(--border)}
.lesson:last-child{border-bottom:0}
.lesson-title{color:var(--text);font-size:16px;font-weight:700;margin-bottom:8px}
.lesson-meta{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;align-items:center;font-size:11px;color:var(--text-3)}
.rep-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--accent);background:var(--accent-bg);border:1px solid var(--border);border-radius:4px;font-family:var(--font)}
.rep-chip a{color:inherit;text-decoration:none}
.tag-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--text-3);border:1px solid var(--border);border-radius:4px}
.lesson-dates{margin-left:auto;color:var(--text-3);font-size:10px;letter-spacing:.06em;text-transform:uppercase}
.lesson-body{color:var(--text-2);font-size:13px;line-height:1.6}
.lesson-body p{margin-bottom:10px}
.lesson-body p:last-child{margin-bottom:0}
.lesson-body .wl-rep{color:var(--accent);font-weight:700;border-bottom:1px dotted var(--accent)}
.lesson-body .wl-lesson{color:#7e22ce;border-bottom:1px dotted #7e22ce}
.empty{color:var(--text-3);padding:48px 0;text-align:center}
</style>
```

- [ ] **Step 3: Verify**

Open http://localhost:3000/lessons.html — page should render with light background, Inter font, indigo links. The breadcrumb `← Dashboard` link leads back to index.html correctly.

- [ ] **Step 4: Commit**

```bash
git add docs/lessons.html
git commit -m "feat(redesign): apply light theme to lessons.html"
```

---

## Task 9: Document image field, verify parity, swap files

**Files:**
- Modify: `REPS_YAML_SPEC.md`
- Rename: `docs/index-v2.html` → `docs/index.html`

- [ ] **Step 1: Update REPS_YAML_SPEC.md — add image field documentation**

In `REPS_YAML_SPEC.md`, find the optional fields section (the block describing `links` and `timeline`). Add `image` to the optional fields schema block:

```yaml
    image:       # string or null — URL or relative path to a logo/screenshot image
                 # e.g. "docs/images/002.jpg" or "https://example.com/logo.png"
                 # Omit if no image. Falls back to GitHub repo logo lookup then letter avatar.
```

In the **Rules** section, add after rule 11 (timeline):

> **12. image** — Optional. A URL or relative path (`docs/images/NNN.{ext}`) pointing to a logo or screenshot for this rep. Displayed as the card image on the dashboard. When absent, the dashboard first checks for common logo filenames in the `repo` (e.g., `logo.png`), then falls back to a letter avatar. Omit the field entirely if no image is available. Store screenshots in `docs/images/` using the rep ID as the filename.

- [ ] **Step 2: Run the full verification checklist**

Open http://localhost:3000/index-v2.html and confirm each item:

- [ ] All reps render with correct status badges and PITA values
- [ ] All 6 status filter pills + "All" filter the grid correctly
- [ ] Search filters by name and summary text
- [ ] Keyboard nav: `j`/`k` moves selection, `Enter` expands, `Esc` collapses
- [ ] Numeric shortcuts: `1` filters idea, `2` assessed, `3` building, `4` live, `5` pmf, `6` dead, `0` all
- [ ] `?` opens help overlay; `Esc` closes it
- [ ] Detail expander: summary, next step, blocker (if any), links, field notes, timeline all present
- [ ] Timeline shows git commits + milestones; "show N more" toggle works
- [ ] Journal sidebar shows field notes; newest entry expanded, older entries preview
- [ ] Rep chips in journal click through to the correct card
- [ ] Journal collapse (`«`) and expand work; state persists in localStorage
- [ ] Reps with >14 days stale show amber day count on card
- [ ] Auto-refresh polls every 5 minutes (check Network tab)
- [ ] `lessons.html` opens correctly with matching light theme

- [ ] **Step 3: Swap index-v2.html to index.html**

```bash
mv docs/index-v2.html docs/index.html
```

- [ ] **Step 4: Verify live file at the standard URL**

```
npm run dev
```
Open http://localhost:3000 — confirm the redesigned dashboard loads at the root URL.

- [ ] **Step 5: Commit everything**

```bash
git add docs/index.html docs/lessons.html REPS_YAML_SPEC.md
git commit -m "$(cat <<'EOF'
feat: ship light-theme dashboard redesign

- Replaces dark terminal aesthetic with clean card-based light design
- Inter font, indigo (#4f46e5) accent, off-white (#f5f5ff) background
- 3-col card grid (2 tablet / 1 mobile) replaces table layout
- Full-width detail expander replaces inline table row expand
- Field notes journal panel moved to right side
- Image loading: GitHub repo logo → image field → letter avatar fallback
- lessons.html updated to matching light theme
- REPS_YAML_SPEC.md documents optional image field

All existing functionality preserved: filtering, sorting, search,
keyboard nav, timeline, field notes, journal collapse, auto-refresh.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Push and verify on GitHub Pages**

```bash
git push
```

Wait ~60 seconds, then open https://100repsproject.com and confirm the redesign is live.
