"""Final retry for last 4 missing portraits."""
import json
import urllib.request
import urllib.parse
import os
import time
import ssl

portraits_dir = os.path.join('data', 'portraits')
os.makedirs(portraits_dir, exist_ok=True)

with open('data/wiki_portraits_result.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

ctx = ssl.create_default_context()

# Try different search terms for missing ones
RETRY = {
    'zhangzai': [('张载', 'zh'), ('Zhang Zai', 'en')],
    'chenghao': [('程颢', 'zh'), ('Cheng Hao', 'en')],
    'lu_jiuyuan': [('陆九渊', 'zh'), ('Lu Jiuyuan', 'en')],
    'kangyouwei': [('康有为', 'zh'), ('Kang Youwei', 'en')],
}

for phil_id, tries in RETRY.items():
    found = False
    for title, lang in tries:
        print(f'  {phil_id} ({title}, {lang})...', end=' ', flush=True)
        wiki = f'https://{lang}.wikipedia.org'
        url = f'{wiki}/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=250'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'PhilographBot/1.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for pid, pdata in pages.items():
                thumb = pdata.get('thumbnail', {}).get('source')
                if thumb:
                    # Download
                    req2 = urllib.request.Request(thumb, headers={'User-Agent': 'PhilographBot/1.0'})
                    with urllib.request.urlopen(req2, context=ctx, timeout=20) as resp2:
                        img_data = resp2.read()
                    local_path = os.path.join(portraits_dir, f'{phil_id}.jpg')
                    with open(local_path, 'wb') as f:
                        f.write(img_data)
                    results[phil_id] = f'data/portraits/{phil_id}.jpg'
                    print(f'OK ({len(img_data)} bytes)')
                    found = True
                    break
                else:
                    print('No thumbnail')
        except Exception as e:
            print(f'Error: {e}')
        if found:
            break
        time.sleep(2)
    if not found:
        print(f'  {phil_id} -> NOT AVAILABLE on Wikipedia')

with open('data/wiki_portraits_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

local_count = sum(1 for v in results.values() if v.startswith('data/'))
remaining = [k for k, v in results.items() if not v.startswith('data/')]
print(f'\nFinal: {local_count} local portraits ready')
print(f'Still missing: {remaining}')
