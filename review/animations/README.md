# Animation experiment browser evidence

Captured from the `codex/ai-divide-animations` worktree at a 1366×768 viewport after each Streamlit route finished rendering. The six `*-viewport.png` files are settled-page views; `before-overview-viewport.png` is the stable redesign's Overview capture at the same viewport. `entrance.gif` shows the Overview page entrance captured over the first few hundred milliseconds.

The motion system uses CSS opacity and an 8px upward settle, 320–340ms; KPI cards are staggered by 60ms. Hover and focus transitions are 160–180ms. Plotly figures receive a native 240ms cubic-in-out transition. `prefers-reduced-motion: reduce` disables animation and transition CSS.

Browser verification confirmed page-entry motion when navigating between pages, no re-entry on a year-filter rerun, KPI hover emphasis, all six routes rendered, and no horizontal overflow at 1366×768. The browser automation surface did not expose reduced-motion emulation, so that preference was checked in the stylesheet but could not be toggled in-browser during this run.
