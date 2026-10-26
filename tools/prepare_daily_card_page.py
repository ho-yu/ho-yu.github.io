"""Prepare reviewable Notion Markdown after rendering and uploading a daily card."""
import argparse
import hashlib
import json
from pathlib import Path

def page_content(data, upload):
    parts=[upload['suggested_markdown'],f'<mention-date start="{data["date"]}"/>',
           '<details>\n<summary>텍스트로 다시 읽기</summary>',
           '\t### 오늘의 핵심','\t'+data['summary']]
    for section in data['sections']:
        parts.extend(['\t### '+section['title'],*['\t'+p for p in section['body']]])
        example=section.get('example')
        if example:
            parts.extend(['\t```python\n'+'\n'.join('\t'+line for line in example['code'].splitlines())+'\n\t```',
                          '\t'+example.get('explanation','')])
    parts.extend(['\t### 기억할 한 줄','\t'+data['remember'],'</details>','## 참고한 기록'])
    for source in data['sources']:
        url=source.get('url',source.get('ref',''))
        if source['kind']=='notion':parts.append(f'- <mention-page url="{url}"/>')
        elif url.startswith('https://'):parts.append(f'- [{source["title"]}]({url})')
        else:parts.append(f'- {source["title"]} · 프로젝트 원문 `{source["ref"]}`')
    parts.extend(['<details>\n<summary>개념·도식 검증 근거와 보정 사항</summary>',
                  '\t검증 기준일: <mention-date start="'+data['verification']['checked_at']+'"/>',
                  '\t학습 기록에서 주제를 고르고, 교안 없이도 적용할 수 있는 일반 정의·원리·조건을 아래 1차 자료로 대조했습니다. 특정 수치와 설정은 필요한 경우에만 예시로 구분합니다.'])
    for section in data['sections']:
        v=section['verification']
        parts.extend(['\t### '+section['title'],'\t'+v['claim']])
        if v.get('note'):parts.append('\t'+v['note'])
        for ref in v['sources']:parts.append(f'\t- [{ref["title"]}]({ref["url"]})')
    corrections=data['verification'].get('corrections',[])
    if corrections:
        parts.append('\t### 정확성을 위해 보정한 내용')
        parts.extend('\t- '+c for c in corrections)
    parts.append('</details>')
    return '\n\n'.join(parts)

def prepare(folder):
    folder=Path(folder)
    data=json.loads((folder/'card.json').read_text(encoding='utf-8-sig'))
    upload=json.loads((folder/'upload.json').read_text(encoding='utf-8'))
    rendered=json.loads((folder/'render.json').read_text(encoding='utf-8'))
    current_hash=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    if current_hash!=rendered.get('data_sha256'):raise ValueError('Card changed since image rendering; regenerate and upload again')
    if data.get('verification',{}).get('status')!='verified' or not rendered.get('visual_reviewed'):
        raise ValueError('Content and visual review must finish before page preparation')
    if upload.get('image_sha256')!=rendered['image_sha256']:raise ValueError('Upload does not match latest image')
    content=page_content(data,upload)
    payload={'properties':{'title':data['date']+' 데일리 학습 카드'},'icon':'📘','content':content}
    (folder/'page.md').write_text(content,encoding='utf-8')
    (folder/'notion-payload.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'date':data['date'],'payload':payload}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('folders',nargs='+')
    args=parser.parse_args()
    print(json.dumps([prepare(p) for p in args.folders],ensure_ascii=True))
