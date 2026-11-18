# Visual accessibility review

## Method

Reviewed 1366×768 browser screenshots of all six pages and generated full-severity protanopia and deuteranopia previews with `scripts/simulate_cvd_review.py`. The script applies the linear-RGB dichromacy matrices from Machado, Oliveira and Fernandes, “A physiologically-based model for simulation of color vision deficiency” (2009), [doi:10.1109/TVCG.2009.113](https://doi.org/10.1109/TVCG.2009.113). The source images were captured during the existing Playwright visual audit and are in `review/animations/`. The generated comparisons are audit aids, not a substitute for evaluation by people with colour-vision deficiency.

The source screenshots predate this audit's correction to hide the unsampled 2022 axis tick. That change only alters tick labels; chart colours, data marks and direct labels are unchanged. AppTest confirms that updated time-series axes show only the four observed survey years.

## Evidence and findings

| Page / visual | Review image | Finding under protanopia and deuteranopia simulation |
|---|---|---|
| Overview and its trend | [Comparison](../review/accessibility/overview-cvd-review.jpg) | Single teal series, labelled year/value and axes; colour is not the only carrier. |
| Country ranking and trend | [Comparison](../review/accessibility/country-cvd-review.jpg) | Ranking values and countries are printed. The EU reference is labelled; trend lines also differ by dash pattern and marker shape. |
| Company-size bars and trend | [Comparison](../review/accessibility/company_size-cvd-review.jpg) | Size classes are named, values printed, and trend series use distinct dash patterns and marker shapes. Similar simulated hues remain identifiable by labels and position. |
| Industry heatmap and ranking | [Comparison](../review/accessibility/industry-cvd-review.jpg) | The heatmap is a single-hue light-to-dark sequential scale rather than red/green; every available tile has a printed value. Ranking bars also have sector labels and numbers. |
| Barrier ranking | [Comparison](../review/accessibility/barrier_ranking-cvd-review.jpg) | Barrier names and values are printed; it is a single-series chart. |
| Barrier comparisons | [Comparison](../review/accessibility/barrier_comparison-cvd-review.jpg) | Country/EU series use named legend entries, printed values and a table with percentage-point differences. The paired bar order and positions remain consistent when hues shift. |
| Conclusion & Sources | [Comparison](../review/accessibility/conclusion-cvd-review.jpg) | Key evidence is stated in text and metric cards; colour does not encode the conclusion. |

The shared text colours were checked against their page backgrounds using the WCAG relative-luminance contrast formula. Body/muted text `#52677A` is 5.40:1 on `#F3F6F8` and 5.87:1 on white; primary text `#17324D` is 13.13:1 on white; sidebar text `#E6F0F2` is 12.46:1 on navy `#102B45`; teal `#007E87` is 4.85:1 on white. Copper `#B65F3D` is 4.47:1 on white and is used for a chart mark, not small text; chart labels use the dark primary text colour. Company-size small-series teal `#659B9D` is 3.12:1 against white and is accompanied by category labels and direct values.

**Result:** The simulated views remain interpretable without distinguishing red from green. All data comparisons retain a second cue such as direct values, named categories, position, line pattern, marker shape or a numeric table. No chart-colour changes were necessary. Streamlit's usual keyboard-accessible controls are retained. `src/ui.py` includes a `prefers-reduced-motion: reduce` media rule that disables nonessential transitions and animations; no new motion was added during this audit.

To regenerate the comparison images after changing the source screenshots:

```sh
python scripts/simulate_cvd_review.py
```

This utility uses Pillow and NumPy, which are already installed with the project's Streamlit requirements in the tested environment.
