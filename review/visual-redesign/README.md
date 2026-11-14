# Visual redesign review

The `before/` images show commit `1934308` and the `after/` images show the redesigned dashboard. Each folder has a `*-viewport.png` (the initial 1366 × 768 browser viewport) and a `*-full.png` (the complete Streamlit page assembled from actual browser scroll captures) for all six pages. `measurements.json` records the main panel's scroll geometry; its `scrollWidth` matched `clientWidth` on every page.

The review used the local Streamlit app in a real browser at 1366 × 768. Each page was navigated and scrolled, charts were allowed to render, and the screenshots were visually inspected. Browser checks also exercised the Industry Divide sector clear/select controls and the Adoption Barriers enterprise-size filter. The heatmap year labels were refined after comparing the first after-capture with the baseline.

The shared palette was checked for text contrast on its principal backgrounds (5.18:1 or better in the measured combinations). Country and size trend lines also differ by dash and marker shape. This is a focused visual check, not a full accessibility audit or a complete colour-vision simulation.
