#!/usr/bin/env python3
"""Fetch complete official JSON-stat cubes and supporting source pages, preserving snapshots."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
BASE = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
SOURCES = {d: BASE + d + '?lang=EN' for d in ('isoc_eb_ai', 'isoc_eb_ain2')}
SOURCES.update({
    'reference_probe': BASE + 'isoc_eb_ai?lang=EN&freq=A&size_emp=GE10&nace_r2=C10-S951_X_K&indic_is=E_AI_BLE&unit=PC_ENT_AI_EC&geo=EU27_2020&time=2025',
    'definition_change_news': 'https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2',
    'publication': 'https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises',
    'methodology': 'https://ec.europa.eu/eurostat/cache/metadata/en/isoc_e_esms.htm',
    'api_guide': 'https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-getting-started/api',
})


def fetch(url):
    for attempt in range(6):
        try:
            request = Request(url, headers={'User-Agent': 'University-AI-Divide-research/1.0', 'Accept': '*/*'})
            with urlopen(request, timeout=300) as response:
                chunks, count = [], 0
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    count += len(chunk)
                    if count > 250 * 1024 * 1024:
                        raise ValueError('Response exceeds 250 MiB; partition official query before retrying')
                    chunks.append(chunk)
                return b''.join(chunks), dict(response.headers)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            if isinstance(exc, HTTPError) and exc.code not in (408, 429, 500, 502, 503, 504):
                raise
            if attempt == 5:
                raise
            retry_after = exc.headers.get('Retry-After', '') if isinstance(exc, HTTPError) else ''
            delay = min(120, int(retry_after)) if retry_after.isdigit() else min(60, 2 ** (attempt + 1))
            print(f'Retry {attempt + 1}: {exc}; waiting {delay}s', flush=True)
            time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Fetch new snapshots; retain earlier originals')
    args = parser.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    manifest_path = RAW / 'manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for name, url in SOURCES.items():
        if name in manifest and not args.refresh:
            path = ROOT / manifest[name]['file']
            if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == manifest[name]['sha256']:
                print(f'Using verified snapshot: {path.name}')
                continue
        payload, headers = fetch(url)
        suffix = 'json' if name.startswith('isoc_') or name == 'reference_probe' else 'html'
        if suffix == 'json':
            cube = json.loads(payload)
            if cube.get('class') != 'dataset' or not cube.get('dimension') or 'value' not in cube:
                raise ValueError(f'Invalid or asynchronous API response for {name}: {str(cube)[:500]}')
        digest = hashlib.sha256(payload).hexdigest()
        path = RAW / f'{name}_{digest[:16]}.{suffix}'
        if path.exists() and path.read_bytes() != payload:
            raise ValueError('Snapshot hash collision')
        if not path.exists():
            path.write_bytes(payload)
        manifest[name] = {'url': url, 'file': str(path.relative_to(ROOT)), 'sha256': digest,
                          'bytes': len(payload), 'retrieved_utc': datetime.now(timezone.utc).isoformat(),
                          'last_modified': headers.get('Last-Modified'), 'etag': headers.get('ETag')}
        temp = manifest_path.with_suffix('.tmp')
        temp.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        temp.replace(manifest_path)
        print(f'Downloaded {name}: {len(payload):,} bytes', flush=True)

if __name__ == '__main__':
    main()
