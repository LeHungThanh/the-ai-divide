#!/usr/bin/env python3
"""Prepare four tidy datasets from full JSON-stat snapshots; no imputation."""
import csv
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNTRIES = set('AT BE BG HR CY CZ DK EE FI FR DE EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE EU27_2020'.split())
YEARS = {'2021', '2023', '2024', '2025'}
OVERALL = 'C10-S951_X_K'
FILES = ['01_country_adoption.csv', '02_company_size.csv', '03_industry_adoption.csv', '04_ai_adoption_barriers.csv']
# NACE section partition, plus the only covered S activity. D/E kept separate.
COMPARISON = set('C D E F G H I J L M N S951'.split())
COLUMNS = ['country_code', 'country_name', 'year', 'freq', 'size_emp', 'size_label',
           'nace_r2', 'industry_label', 'industry_level', 'is_comparison_sector',
           'indicator_code', 'indicator_label', 'unit', 'unit_label', 'denominator_definition',
           'percentage', 'observation_status', 'status_label', 'source_dataset', 'source_url',
           'source_updated', 'retrieved_utc', 'raw_file', 'raw_sha256', 'source_observation_index']


def load_cube(dataset):
    manifest = json.loads((ROOT / 'data/raw/manifest.json').read_text())
    meta = manifest[dataset]
    return json.loads((ROOT / meta['file']).read_text()), meta


def codes(cube, dim):
    cache = cube.setdefault('_ordered_codes', {})
    if dim not in cache:
        index = cube['dimension'][dim]['category']['index']
        cache[dim] = sorted(index, key=index.get) if isinstance(index, dict) else index
    return cache[dim]


def item_at(container, index, default=None):
    if isinstance(container, list):
        return container[index] if index < len(container) and container[index] is not None else default
    return container.get(str(index), default)


def source_index(cube, key):
    positions = cube.setdefault('_code_positions', {})
    index = 0
    for dim, length in zip(cube['id'], cube['size']):
        if dim not in positions:
            positions[dim] = {c: i for i, c in enumerate(codes(cube, dim))}
        index = index * length + positions[dim][key[dim]]
    return index


def barrier_codes(cube):
    labels = cube['dimension']['indic_is']['category']['label']
    return [c for c in codes(cube, 'indic_is') if labels[c].startswith('Enterprises do not use AI technologies, because')]


def make_row(cube, meta, ds, key):
    def label(dim):
        return cube['dimension'][dim]['category'].get('label', {}).get(key[dim], key[dim])
    index = source_index(cube, key)
    value = item_at(cube['value'], index)
    flag = item_at(cube.get('status', {}), index, '')
    nace = key['nace_r2']
    level = ('overall_aggregate' if nace == OVERALL else 'section' if len(nace) == 1
             else 'division' if len(nace) == 3 and nace[1:].isdigit()
             else 'group' if nace == 'S951' else 'overlapping_group')
    denominator = label('unit')
    if key['unit'] == 'PC_ENT_AI_EC':
        denominator += '; for barrier indicators: non-users who ever considered using AI; not all enterprises'
    return dict(zip(COLUMNS, [key['geo'], label('geo'), key['time'], key['freq'], key['size_emp'], label('size_emp'),
          nace, label('nace_r2'), level, str(nace in COMPARISON).lower(), key['indic_is'], label('indic_is'),
          key['unit'], label('unit'), denominator, '' if value is None else value, flag,
          cube.get('extension', {}).get('status', {}).get('label', {}).get(flag, flag),
          ds, meta['url'], cube.get('updated', ''), meta['retrieved_utc'], meta['file'], meta['sha256'], index]))


def selected_rows(number):
    ds = 'isoc_eb_ain2' if number == 3 else 'isoc_eb_ai'
    cube, meta = load_cube(ds)
    # Metadata codes are discovered before selection, and all selections must be present.
    assert COUNTRIES <= set(codes(cube, 'geo'))
    assert YEARS <= set(codes(cube, 'time'))
    sizes = ['GE10'] if number in (1, 3) else codes(cube, 'size_emp')
    industries = codes(cube, 'nace_r2') if number == 3 else [OVERALL]
    indicators = barrier_codes(cube) if number == 4 else ['E_AI_TANY']
    units = ['PC_ENT']
    if number == 4:
        # Discover which unit planes actually carry barrier observations/statuses.
        units = []
        for unit in codes(cube, 'unit'):
            found = False
            for size, indicator, geo, year in itertools.product(sizes, indicators, codes(cube, 'geo'), codes(cube, 'time')):
                k = dict(freq='A', size_emp=size, nace_r2=OVERALL, indic_is=indicator, unit=unit, geo=geo, time=year)
                idx = source_index(cube, k)
                if item_at(cube['value'], idx) is not None or item_at(cube.get('status', {}), idx):
                    found = True
                    break
            if found:
                units.append(unit)
    for dim, selection in [('size_emp', sizes), ('nace_r2', industries), ('indic_is', indicators), ('unit', units)]:
        assert set(selection) <= set(codes(cube, dim)), (dim, selection)
    for geo, year, size, nace, indicator, unit in itertools.product(sorted(COUNTRIES), sorted(YEARS), sizes, industries, indicators, units):
        key = dict(freq='A', size_emp=size, nace_r2=nace, indic_is=indicator, unit=unit, geo=geo, time=year)
        yield make_row(cube, meta, ds, key)



def write_dictionary():
    cube, _ = load_cube('isoc_eb_ai')
    industry_cube, _ = load_cube('isoc_eb_ain2')
    descriptions = {
        'country_code': 'Eurostat geography identifier; EL=Greece; EU27_2020 is an aggregate.',
        'country_name': 'Official English geography label.',
        'year': 'Integer survey year: 2021, 2023, 2024 or 2025; annual, not an interpolated series.',
        'freq': 'Official frequency code A (annual).',
        'size_emp': 'Official persons-employed size code; includes employees and self-employed persons.',
        'size_label': 'Official size definition; codes are retained verbatim.',
        'nace_r2': 'Official NACE Rev. 2 activity or aggregate identifier.',
        'industry_label': 'Official activity label; use methodology for exact survey coverage.',
        'industry_level': 'overall_aggregate, section, division, group, or overlapping_group; sections also aggregate their subdivisions.',
        'is_comparison_sector': 'Lowercase true/false. True selects C,D,E,F,G,H,I,J,L,M,N,S951 without overlaps.',
        'indicator_code': 'E_AI_TANY for adoption; eight metadata-discovered reason codes for barriers.',
        'indicator_label': 'Official current English indicator definition; not a per-year questionnaire label.',
        'unit': 'Official unit code; part of the statistical key, never combine different units.',
        'unit_label': 'Exact official percentage unit label.',
        'denominator_definition': 'Official unit population, with considered-but-not-adopted clarification for PC_ENT_AI_EC barrier rows. Always conditional on row geography, activity and size.',
        'percentage': 'Numeric percentage, 0–100, decimal point. Empty = unavailable/suppressed/uncollected; never zero-filled.',
        'observation_status': 'Verbatim source flag, including combinations and punctuation. Empty = no source flag, not proof of availability.',
        'status_label': 'Official description of the whole flag string; empty if unflagged.',
        'source_dataset': 'isoc_eb_ai or isoc_eb_ain2.',
        'source_url': 'Full official API request from selected raw manifest.',
        'source_updated': 'Source dataset update timestamp from JSON-stat metadata, not observation year.',
        'retrieved_utc': 'UTC acquisition timestamp from manifest.',
        'raw_file': 'Repository-relative path to exact unmodified raw JSON response.',
        'raw_sha256': 'SHA-256 of original response bytes; verifies reproducibility.',
        'source_observation_index': 'Zero-based flattened JSON-stat cell index. Absent value at this index means missing; this is a cube address, not an observed row number.',
    }
    lines = ['# Data dictionary', '',
             'The four CSVs share 25 columns. Encoding: UTF-8; delimiter: comma; decimal separator: point. Booleans are lowercase text. Missing numeric values are empty fields.', '',
             'Primary key / composite observation identifier: `country_code, year, freq, size_emp, nace_r2, indicator_code, unit`. Values are percentages on a 0–100 scale; 19.95 means 19.95%, not 0.1995.', '',
             '## Dataset catalogue', '',
             '| Output CSV | Purpose | Official source and direct API URL | Geographic / time coverage | Latest observation example |',
             '|---|---|---|---|---|',
             '| `01_country_adoption.csv` | Overall enterprise AI adoption by EU country and supplied EU aggregate. | [isoc_eb_ai](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=EN) | EU27 + EU27_2020; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, GE10, `E_AI_TANY`, `PC_ENT`: **19.95%**. |',
             '| `02_company_size.csv` | Adoption by country and official enterprise employment-size class. | [isoc_eb_ai](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=EN) | EU27 + EU27_2020 and retained size classes; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, `GE250`, `E_AI_TANY`, `PC_ENT`: **55.03%** (small 10–49: 17.00%; medium 50–249: 30.36%). |',
             '| `03_industry_adoption.csv` | Adoption by country and NACE Rev. 2 activity, including aggregates and non-overlapping comparison partition. | [isoc_eb_ain2](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ain2?lang=EN) | EU27 + EU27_2020 and all source NACE categories; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, sector J, `E_AI_TANY`, `PC_ENT`: **62.52%**. |',
             '| `04_ai_adoption_barriers.csv` | Eight reasons for AI non-adoption across size, country and four distinct denominator units. | [isoc_eb_ai](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=EN) | EU27 + EU27_2020 and source size classes; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, GE10, `E_AI_BLE`, `PC_ENT_AI_EC`: **70.31%** (considered AI but did not adopt). |', '',
             'All four are Eurostat statistical data. Eurostat’s [reuse notice](https://ec.europa.eu/eurostat/help/copyright-notice) authorises reuse of statistical data and metadata with source acknowledgement, subject to individual notices and listed exceptions; it implements Commission Decision 2011/833/EU. This is not described as a blanket CC BY 4.0 licence for datasets. The notice separately says editorial website content is CC BY 4.0. No contrary dataset-specific notice was present in the bundled cube metadata; users should check the live dataset notice before other reuse.', '',
             'Source files are exact JSON-stat API responses stored in `data/raw/`; retrieval URL, timestamp, response byte size and SHA-256 are in `data/raw/manifest.json`. The source API reports an update timestamp of 15 June 2026. The source survey covers enterprises in specified activities; the standard comparison population is enterprises with at least 10 persons employed, excluding agriculture, mining and finance.', '',
             'Transformation: `scripts/prepare_data.py` selects the retained geographies and four actually available survey years from source dimensions, preserves an explicit grid of missing combinations, reads each value/status at its JSON-stat flattened index and writes the columns below. No interpolation, zero-fill, EU averaging or synthetic rows with non-missing percentages are used. Source flags are retained verbatim. Empty percentages mean unavailable, uncollected or suppressed; the source may not distinguish these causes.', '',
             '| Column | Definition |', '|---|---|']
    lines += [f'| {c} | {descriptions[c]} |' for c in COLUMNS]
    for title, source, dim, selected in [
        ('Official size classifications', cube, 'size_emp', codes(cube, 'size_emp')),
        ('Units and denominator definitions (full raw metadata)', cube, 'unit', codes(cube, 'unit')),
        ('AI adoption and all non-adoption barriers', cube, 'indic_is', ['E_AI_TANY'] + barrier_codes(cube)),
        ('All industry categories', industry_cube, 'nace_r2', codes(industry_cube, 'nace_r2')),
        ('Geographies retained', cube, 'geo', sorted(COUNTRIES)),
    ]:
        lines += ['', f'## {title}', '', '| Code | Official English label |', '|---|---|']
        labels = source['dimension'][dim]['category']['label']
        lines += [f'| {c} | {labels[c]} |' for c in selected]
    lines += ['', '## Source observation flags', '', '| Code | Official meaning |', '|---|---|']
    flags = {}
    for source in (cube, industry_cube):
        flags.update(source.get('extension', {}).get('status', {}).get('label', {}))
    lines += [f'| {c.replace(chr(124), "&#124;")} | {label.replace(chr(124), "&#124;")} |' for c, label in flags.items()]
    lines += ['', '## Analysis rules', '',
              '- Size comparisons: 10-49 (small), 50-249 (medium), GE250 (large). GE10 and 10-249 overlap these sizes; microenterprise classes are optional and sparse.',
              '- Industry comparisons: filter is_comparison_sector=true. All other industry rows are retained for drilldown and overlap parts of the comparison partition. A section and its divisions must not be summed.',
              '- Barrier comparisons: fix the unit, size and activity. PC_ENT_AI_EC means the considered-but-not-adopted group; PC_ENT_AI_TX means all non-users; PC_ENT means all enterprises in scope; PC_ENT_IUSE means the internet-access population.',
              '- Unit definitions for PC_ENT_AI_TANY and PC_ENT_AI_PDI are included from full metadata for transparency but are not applicable barrier output planes in this snapshot.',
              '- Percentages across countries or industries require statistical weights to aggregate. EU values are supplied by Eurostat, not computed as country means.',
              '- Keep flags with charts and report missing coverage. See data_sources.md for questionnaire changes and data_validation_report.md for the publication-vintage discrepancy.']
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs/data_dictionary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    write_dictionary()
    out = ROOT / 'data/processed'
    out.mkdir(parents=True, exist_ok=True)
    for n, filename in enumerate(FILES, 1):
        rows = list(selected_rows(n))
        path = out / filename
        temp = path.with_suffix('.tmp')
        with temp.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        temp.replace(path)
        print(f'{filename}: {len(rows):,} rows, {sum(r["percentage"] != "" for r in rows):,} non-missing')

if __name__ == '__main__':
    main()
