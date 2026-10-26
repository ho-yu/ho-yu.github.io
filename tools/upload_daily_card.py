"""Upload daily-card PNGs using short-lived URLs returned by the Notion connector.

Read one JSON job per stdin line: {"date":"YYYY-MM-DD", "upload":{...tool response...}}.
End with {"finish":true}. Authentication is kept in memory and never written to disk.
"""
from datetime import date
import json
import hashlib
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1] / 'workspace' / 'daily-cards'


def upload(job):
    day = date.fromisoformat(job['date']).isoformat()
    spec = job['upload']
    address = urlsplit(spec['upload_url'])
    if address.scheme != 'https' or address.hostname != 'api.notion.com':
        raise ValueError('Expected the official Notion upload endpoint')
    source = (ROOT / day / f'{day}-daily-card.png').resolve()
    if not source.is_relative_to(ROOT.resolve()):
        raise ValueError('Image must be inside the daily-card workspace')
    binary = source.read_bytes()
    if not binary.startswith(b'\x89PNG\r\n\x1a\n') or len(binary) > 20 * 1024 * 1024:
        raise ValueError('Expected a PNG no larger than 20 MiB')
    card = json.loads(source.with_name('card.json').read_text(encoding='utf-8-sig'))
    rendered = json.loads(source.with_name('render.json').read_text(encoding='utf-8'))
    data_hash = hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if card.get('verification', {}).get('status') != 'verified':
        raise ValueError('Content verification is incomplete')
    if rendered.get('data_sha256') != data_hash or rendered.get('image_sha256') != hashlib.sha256(binary).hexdigest():
        raise ValueError('Card changed since rendering; regenerate and inspect before uploading')
    if rendered.get('diagrams') != len(card['sections']) or not rendered.get('visual_reviewed'):
        raise ValueError('Every concept needs a diagram and the final image must be visually reviewed')
    boundary = '----DailyCard' + uuid4().hex
    field = spec.get('upload_form_field', 'file')
    if field != 'file':
        raise ValueError('Unexpected file form field')
    opening = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
               f'filename="{source.name}"\r\nContent-Type: image/png\r\n\r\n').encode()
    body = opening + binary + f'\r\n--{boundary}--\r\n'.encode()
    headers = dict(spec['upload_headers'])
    headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
    request = Request(spec['upload_url'], data=body, headers=headers, method='POST')
    # Exactly one POST per connector-created upload; never silently retry.
    with urlopen(request, timeout=45) as response:
        result = json.load(response)
    if not result.get('suggested_markdown'):
        raise ValueError('Upload returned no embeddable Markdown')
    receipt = {key: result.get(key) for key in ('markdown_source', 'suggested_markdown')}
    receipt.update(date=day, file_upload_id=spec['file_upload_id'], image_sha256=rendered['image_sha256'], style=rendered['style'])
    source.with_name('upload.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    return receipt


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        job = json.loads(line)
        if job.get('finish'):
            break
        try:
            result = upload(job)
            print(json.dumps(result, ensure_ascii=True), flush=True)
        except HTTPError as exc:
            print(json.dumps({'date': job.get('date'), 'error': f'HTTP {exc.code}'}), flush=True)
        except URLError as exc:
            print(json.dumps({'date': job.get('date'), 'error': 'Network failure',
                              'reason': str(exc.reason)}), flush=True)
        except Exception as exc:
            print(json.dumps({'date': job.get('date'), 'error': str(exc)}), flush=True)


if __name__ == '__main__':
    main()
