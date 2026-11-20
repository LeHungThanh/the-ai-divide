# Animation, layout and Adoption Barriers evidence

The six `*-viewport.png` files are settled 1366×768 views of the dashboard. `entrance.gif` records the Overview page transition; `barriers-after-viewport.png` and `barriers-after-section-3.png` show the Adoption Barriers ranking and comparison views used by the colour-vision review. These images are retained as supporting evidence for the accessibility review.

The shared motion system uses a CSS opacity and 8px upward settle over 320–340ms, staggered KPI cards, and 160–180ms hover/focus transitions. Adoption Barriers uses the shared page-entry treatment and native chart hover, while disabling Plotly data interpolation on redraw to keep filter updates stable. The reduced-motion stylesheet disables nonessential page motion. The other pages retain a shared 240ms Plotly transition.

The captured browser checks show page-entry motion on navigation, no entrance replay after filter reruns, a responsive layout without horizontal overflow, and working filters. The Adoption Barriers page compares the 10–49 and 250+ enterprise groups and compares a Member State with Eurostat's official EU27 aggregate. Its tables show exact values and signed percentage-point gaps; plotted marks omit missing observations. Source details and quality flags remain accessible in the application.
