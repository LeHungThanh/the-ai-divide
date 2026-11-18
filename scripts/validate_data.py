#!/usr/bin/env python3
"""Validate coverage, keys, bounds, metadata, raw traces and published reference values."""
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
import re
from prepare_data import (ROOT, COUNTRIES, YEARS, FILES, COLUMNS, OVERALL, COMPARISON,
                          load_cube, codes, source_index, item_at, selected_rows, barrier_codes)

PUBLICATION = 'https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises'
REFERENCES = [
    (1, 'EU27_2020', 'GE10', 'E_AI_TANY', 'PC_ENT', 19.95),
    (1, 'DK', 'GE10', 'E_AI_TANY', 'PC_ENT', 42.03),
    (1, 'RO', 'GE10', 'E_AI_TANY', 'PC_ENT', 5.21),
    (2, 'EU27_2020', 'GE250', 'E_AI_TANY', 'PC_ENT', 55.03),
    (4, 'EU27_2020', 'GE10', 'E_AI_BLE', 'PC_ENT_AI_EC', 70.89),
]
KEY = ['country_code', 'year', 'freq', 'size_emp', 'nace_r2', 'indicator_code', 'unit']

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, text):
        self.parts.append(text)


def main():
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    manifest = json.loads((ROOT / 'data/raw/manifest.json').read_text())
    lines = ['# Data validation report', '', f'Generated (UTC): {datetime.now(timezone.utc).isoformat()}', '',
             'Reproduce: `python3 scripts/validate_data.py`. Empty percentages mean missing, never zero.', '',
             '## Raw source inventory', '', '| Dataset | Cube cells | Numeric observations | Status entries | Updated |',
             '|---|---:|---:|---:|---|']
    for name, meta in manifest.items():
        content = (ROOT / meta['file']).read_bytes()
        check(hashlib.sha256(content).hexdigest() == meta['sha256'], f'Hash mismatch: {name}')
    for ds in ('isoc_eb_ai', 'isoc_eb_ain2'):
        cube, _ = load_cube(ds)
        vals = cube['value']
        nonmissing = sum(v is not None for v in (vals.values() if isinstance(vals, dict) else vals))
        lines.append(f'| {ds} | {math.prod(cube["size"]):,} | {nonmissing:,} | {len(cube.get("status", {})):,} | {cube["updated"]} |')
    data = {}
    summaries = {}
    for n, filename in enumerate(FILES, 1):
        with (ROOT / 'data/processed' / filename).open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            check(reader.fieldnames == COLUMNS, f'Column mismatch: {filename}')
            rows = list(reader)
        data[n] = rows
        ds = 'isoc_eb_ain2' if n == 3 else 'isoc_eb_ai'
        cube, meta = load_cube(ds)
        keys = [tuple(r[k] for k in KEY) for r in rows]
        duplicates = len(keys) - len(set(keys))
        check(duplicates == 0, f'Duplicate keys: {filename}')
        check(set(r['country_code'] for r in rows) == COUNTRIES, f'Country coverage: {filename}')
        check(set(r['year'] for r in rows) == YEARS, f'Year coverage: {filename}')
        expected = {tuple(str(r[k]) for k in KEY) for r in selected_rows(n)}
        check(set(keys) == expected, f'Incomplete selection grid: {filename}')
        for r in rows:
            k = dict(freq=r['freq'], size_emp=r['size_emp'], nace_r2=r['nace_r2'], indic_is=r['indicator_code'],
                     unit=r['unit'], geo=r['country_code'], time=r['year'])
            idx = source_index(cube, k)
            v = item_at(cube['value'], idx)
            check(r['source_observation_index'] == str(idx), f'Index mismatch: {filename}:{idx}')
            check((r['percentage'] == '' and v is None) or
                  (r['percentage'] != '' and v is not None and float(r['percentage']) == v), f'Raw value mismatch: {filename}:{idx}')
            if r['percentage'] != '':
                check(math.isfinite(float(r['percentage'])) and 0 <= float(r['percentage']) <= 100, f'Out of bounds: {filename}:{idx}')
            check(r['observation_status'] == item_at(cube.get('status', {}), idx, ''), f'Flag mismatch: {filename}:{idx}')
            check(r['unit_label'] == cube['dimension']['unit']['category']['label'][r['unit']], f'Unit label: {filename}:{idx}')
            check(r['raw_sha256'] == meta['sha256'] and r['raw_file'] == meta['file'], f'Provenance mismatch: {filename}:{idx}')
            check(r['source_url'] == meta['url'] and r['source_updated'] == cube['updated'], f'Source metadata mismatch: {filename}:{idx}')
            for col, dim in [('country_name', 'geo'), ('size_label', 'size_emp'), ('industry_label', 'nace_r2'), ('indicator_label', 'indic_is')]:
                check(r[col] == cube['dimension'][dim]['category']['label'][k[dim]], f'Label mismatch: {filename}:{idx}:{col}')
        nonmissing = sum(r['percentage'] != '' for r in rows)
        sizes = sorted({r['size_emp'] for r in rows})
        industries = sorted({r['nace_r2'] for r in rows})
        units = sorted({r['unit'] for r in rows})
        if n == 2:
            check({'10-49', '50-249', 'GE250'} <= set(sizes), 'Required size classes absent')
        if n == 3:
            check(set(industries) == set(codes(cube, 'nace_r2')), 'Industry categories lost')
            check({r['nace_r2'] for r in rows if r['is_comparison_sector'] == 'true'} == COMPARISON, 'Sector partition mismatch')
        if n == 4:
            check({r['indicator_code'] for r in rows} == set(barrier_codes(cube)), 'Barrier indicators lost')
        summary = dict(rows=len(rows), nonmissing=nonmissing, missing=len(rows)-nonmissing,
                       duplicate_keys=duplicates, countries=sorted(COUNTRIES), years=sorted(YEARS),
                       sizes=sizes, industries=industries, units=units,
                       flags=dict(Counter(r['observation_status'] or '(none)' for r in rows)))
        summaries[filename] = summary
        lines += ['', f'## Member {n}: {filename}', '',
                  f'- Rows: **{len(rows):,}**; non-missing: **{nonmissing:,}**; missing: **{len(rows)-nonmissing:,}**; duplicate keys: {duplicates}.',
                  f'- Countries: {", ".join(sorted(COUNTRIES))} (27 countries + EU aggregate).',
                  f'- Years: {", ".join(sorted(YEARS))}.', f'- Sizes: {", ".join(sizes)}.',
                  f'- Industries ({len(industries)}): {", ".join(industries)}.', f'- Units: {", ".join(units)}.',
                  f'- Flags (including missing cells): `{summary["flags"]}`.',
                  '- Every output cell was traced to its JSON-stat index, including missing values and flags.', '',
                  '### Non-missing coverage by year and unit', '', '| Year | Unit | Rows | Non-missing |', '|---|---|---:|---:|']
        for year in sorted(YEARS):
            for unit in units:
                group = [r for r in rows if r['year'] == year and r['unit'] == unit]
                lines.append(f'| {year} | {unit} | {len(group)} | {sum(r["percentage"] != "" for r in group)} |')
        sample = next(r for r in rows if r['percentage'] != '')
        lines += ['', '### Sample raw trace', '', f'Key: `{ {k: sample[k] for k in KEY} }`.',
                  f'Value: {sample["percentage"]}; status: `{sample["observation_status"] or "(none)"}`; raw file: `{sample["raw_file"]}`; '
                  f'JSON-stat `value["{sample["source_observation_index"]}"]`.', '', '### Columns', '', '`' + ', '.join(COLUMNS) + '`', '',
                  '### Five sample observations', '', '| Country | Year | Size | Industry | Indicator | Unit | Percentage | Flag |', '|---|---|---|---|---|---|---:|---|']
        samples = [r for r in rows if r['percentage'] != ''][:5]
        for r in samples:
            lines.append('| ' + ' | '.join(r[c] for c in ['country_code','year','size_emp','nace_r2','indicator_code','unit','percentage','observation_status']) + ' |')
        print(f'\nMember {n}: {filename}\nRows={len(rows)}, non-missing={nonmissing}\nColumns: {", ".join(COLUMNS)}')
        for sample_row in samples:
            print(json.dumps(sample_row, ensure_ascii=False))
    parser = Text()
    parser.feed((ROOT / manifest['publication']['file']).read_text(encoding='utf-8'))
    publication_text = re.sub(r'\s+', ' ', ' '.join(parser.parts))
    integrity_errors = list(errors)
    warnings = []
    probe, probe_meta = json.loads((ROOT / manifest['reference_probe']['file']).read_text()), manifest['reference_probe']
    probe_value = item_at(probe['value'], 0)
    actual_full = next(float(r['percentage']) for r in data[4] if r['country_code'] == 'EU27_2020' and r['year'] == '2025' and r['size_emp'] == 'GE10' and r['indicator_code'] == 'E_AI_BLE' and r['unit'] == 'PC_ENT_AI_EC')
    check(probe_value == actual_full, 'Independent targeted API response differs from full cube')
    integrity_errors = list(errors)
    lines += ['', '## Published 2025 reference checks', '', f'[Official Eurostat publication]({PUBLICATION}) (December 2025 data extraction).', '',
              '| Country | Size | Indicator | Unit | Download | Reference | Result |', '|---|---|---|---|---:|---:|---|']
    reference_results = []
    for n, geo, size, indicator, unit, expected in REFERENCES:
        found = [r for r in data[n] if r['country_code'] == geo and r['year'] == '2025' and r['size_emp'] == size
                 and r['nace_r2'] == OVERALL and r['indicator_code'] == indicator and r['unit'] == unit]
        actual = float(found[0]['percentage']) if len(found) == 1 and found[0]['percentage'] != '' else None
        ok = actual is not None and abs(actual - expected) < 0.005
        known_vintage_difference = (
            (geo, size, indicator, unit, expected, actual)
            == ('EU27_2020', 'GE10', 'E_AI_BLE', 'PC_ENT_AI_EC', 70.89, 70.31)
        )
        if not ok and not known_vintage_difference:
            check(False, f'Reference discrepancy {geo}/{size}/{indicator}/{unit}: {actual} vs {expected}; investigate source selection')
        if known_vintage_difference:
            warnings.append('Documented publication-vintage difference: Eurostat article 70.89 vs June 2026 cube 70.31 for EU27_2020/2025/GE10/E_AI_BLE/PC_ENT_AI_EC; exact revision reason unconfirmed.')
        supported = f'{expected:.2f}' in publication_text
        check(supported, f'Publication snapshot does not contain reference {expected}; inspect source page')
        result = 'PASS' if ok and supported else 'KNOWN SOURCE-VINTAGE DIFFERENCE' if known_vintage_difference and supported else 'FAIL'
        lines.append(f'| {geo} | {size} | {indicator} | {unit} | {actual} | {expected} | {result} |')
        reference_results.append(dict(country=geo, size=size, indicator=indicator, unit=unit, actual=actual, expected=expected, passed=ok and supported, result=result))
    lines += ['', '### Expertise barrier discrepancy investigation', '',
              f'The separate [targeted official API request]({probe_meta["url"]}) returns **{probe_value}%**, confirming the complete-cube observation with the same dimensions and denominator. Its preserved response is `{probe_meta["file"]}`.',
              'The complete source cube was updated on 2026-06-15, after the publication data extraction in December 2025. The difference is -0.58 percentage points. Other EU barrier figures also differ from the article (legal uncertainty: current 53.61 vs published 52.52; privacy: current 52.72 vs published 48.83). This supports a source-vintage/revision explanation, rather than a decoding or unit-selection error. The API does not give a revision reason or a cell-level revision history, so the exact cause remains unconfirmed. The original 70.31 is retained; 70.89 is never substituted.',
              '', '## Interpretation and limitations', '',
              '- Missing grids are explicit: an empty cell can mean unavailable, not collected, or suppressed; a missing flag alone cannot distinguish those reasons.',
              '- Optional microenterprise size classes have sparse national coverage. Use 10-49, 50-249 and GE250 for the standard size comparison; GE10 and 10-249 overlap these groups.',
              '- Barrier observations exist in all four survey years, with availability varying by country and size. See year/unit coverage above. Preserve missing rows; do not impute them.',
              '- Barriers permit multiple responses and do not sum to 100%. The PC_ENT_AI_EC denominator concerns non-users who considered AI; PC_ENT, PC_ENT_IUSE and PC_ENT_AI_TX have different denominators.',
              '- Industry rates cannot be summed or averaged into totals without enterprise weights. Filter is_comparison_sector=true for the non-overlapping sector partition; other rows overlap.',
              '- Eurostat flags include breaks in time series (notably Netherlands 2025), differing definitions, low reliability and confidentiality. Consult source metadata before comparing flagged observations.',
              '- Current category labels are not a historical questionnaire. Language/code generation and image/video/audio generation changed across survey rounds; long-run adoption differences can reflect both uptake and questionnaire changes. No harmonisation or interpolation has been applied.',
              '- EU aggregate is the supplied Eurostat statistic, not an unweighted country average. Survey coverage excludes enterprises below 10 persons for standard comparisons, agriculture, mining, finance and most other S activities.',
              '', '## Result', '', ('Structural, raw-trace, bounds, duplicate and metadata checks: **PASS**.' if not integrity_errors else 'Data integrity checks: **FAIL**.'), '', '**PASS WITH DOCUMENTED PUBLICATION-VINTAGE DIFFERENCE**' if not errors else '**FAIL: data integrity or unexplained reference check**', '']
    lines += [f'- Warning: {warning}' for warning in warnings]
    lines += [f'- Error: {e}' for e in errors]
    report = ROOT / 'docs/data_validation_report.md'
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (ROOT / 'docs/data_validation_summary.json').write_text(json.dumps(dict(outputs=summaries, references=reference_results, integrity_errors=integrity_errors, targeted_probe=probe_value, warnings=warnings, errors=errors, result='PASS_WITH_DOCUMENTED_SOURCE_VINTAGE_DIFFERENCE' if warnings and not errors else 'PASS' if not errors else 'FAIL'), indent=2)+'\n')
    print('\n' + ('PASS with documented publication-vintage difference.' if warnings and not errors else 'PASS: all checks passed.' if not errors else 'FAIL: ' + '; '.join(errors[:20])))
    raise SystemExit(bool(errors))

if __name__ == '__main__':
    main()
