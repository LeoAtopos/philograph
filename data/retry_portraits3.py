"""Retry remaining 21 portraits - fetch thumbnail URLs then download with longer delays."""
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

# Mapping of philosopher ID to their Wikipedia page title for thumbnail lookup
RETRY_MAP = {
    'habermas': ('Jürgen Habermas', 'en'),
    'derrida': ('Jacques Derrida', 'en'),
    'searle': ('John Searle', 'en'),
    'nozick': ('Robert Nozick', 'en'),
    'singer': ('Peter Singer', 'en'),
    'gongsunlong': ('公孙龙', 'zh'),
    'yangxiong': ('扬雄', 'zh'),
    'wangbi': ('王弼', 'zh'),
    'xuanzang': ('玄奘', 'zh'),
    'liuzongyuan': ('柳宗元', 'zh'),
    'zhou_dunyi': ('周敦颐', 'zh'),
    'zhangzai': ('张载', 'zh'),
    'chenghao': ('程颢', 'zh'),
    'lu_jiuyuan': ('陆九渊', 'zh'),
    'daizhen': ('戴震', 'zh'),
    'gongzizhen': ('龚自珍', 'zh'),
    'weiyuan': ('魏源', 'zh'),
    'kangyouwei': ('康有为', 'zh'),
    'liangqichao': ('梁启超', 'zh'),
    'zhangtaiyan': ('章太炎', 'zh'),
    'xiongshili': ('熊十力', 'zh'),
}

def get_thumb_url(title, lang='en'):
    """Get thumbnail URL (250px) from Wikipedia API."""
    wiki = f'https://{lang}.wikipedia.org'
    url = f'{wiki}/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=250'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PhilographBot/1.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        pages = data.get('query', {}).get('pages', {})
        for pid, pdata in pages.items():
            if 'thumbnail' in pdata:
                return pdata['thumbnail']['source']
    except Exception as e:
        print(f'    API error: {e}')
    return None

def download_image(url, filepath):
    """Download image from URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PhilographBot/1.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            with open(filepath, 'wb') as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f'    Download error: {e}')
        return False

# Step 1: Collect all thumbnail URLs first (lightweight API calls)
print("Step 1: Fetching thumbnail URLs...")
thumb_urls = {}
for phil_id, (title, lang) in RETRY_MAP.items():
    safe = title.encode('ascii', 'replace').decode('ascii')
    print(f'  {phil_id} ({safe})...', end=' ', flush=True)
    thumb = get_thumb_url(title, lang)
    if thumb:
        thumb_urls[phil_id] = thumb
        print(f'OK')
    else:
        print('NOT FOUND')
    time.sleep(1)

print(f"\nStep 2: Downloading {len(thumb_urls)} images...")
print()

# Step 2: Download images one by one with longer delays
for phil_id, url in thumb_urls.items():
    print(f'  {phil_id}...', end=' ', flush=True)
    local_path = os.path.join(portraits_dir, f'{phil_id}.jpg')
    if download_image(url, local_path):
        results[phil_id] = f'data/portraits/{phil_id}.jpg'
        print('OK')
    else:
        print('FAILED')
    time.sleep(3)

# Save
with open('data/wiki_portraits_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

local_count = sum(1 for v in results.values() if v.startswith('data/'))
remaining = [k for k, v in results.items() if not v.startswith('data/')]
print(f'\nFinal: {local_count} local portraits ready')
print(f'Still missing: {remaining}')
