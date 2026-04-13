"""Retry remaining portraits using thumbnails (smaller, less likely to be rate-limited)."""
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

# Get entries that still have wikimedia URLs
remaining = {k: v for k, v in results.items() if 'wikimedia' in v}

print(f"Retrying {len(remaining)} portraits with thumbnails (250px)...")
print()

for phil_id, url in remaining.items():
    # Use thumbnail API instead of direct URL to get smaller images
    # Extract filename from URL
    filename = url.split('/commons/')[-1] if '/commons/' in url else url.split('/')[-1]
    
    # Use the Wikipedia thumbnail API to get a 250px version
    thumb_url = f"https://en.wikipedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&iiurlwidth=250&format=json"
    
    print(f'  {phil_id}...', end=' ', flush=True)
    try:
        req = urllib.request.Request(thumb_url, headers={'User-Agent': 'PhilographBot/1.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            imageinfo = page_data.get('imageinfo', [])
            if imageinfo:
                thumb_url_result = imageinfo[0].get('thumburl', imageinfo[0].get('url'))
                if thumb_url_result:
                    # Download the thumbnail
                    req2 = urllib.request.Request(thumb_url_result, headers={'User-Agent': 'PhilographBot/1.0'})
                    with urllib.request.urlopen(req2, context=ctx, timeout=15) as resp2:
                        img_data = resp2.read()
                    local_path = os.path.join(portraits_dir, f'{phil_id}.jpg')
                    with open(local_path, 'wb') as f:
                        f.write(img_data)
                    results[phil_id] = f'data/portraits/{phil_id}.jpg'
                    print(f'OK ({len(img_data)} bytes)')
                else:
                    print('No thumb URL')
            else:
                print('No imageinfo')
    except Exception as e:
        print(f'FAILED: {e}')
    time.sleep(3)  # Longer delay to avoid rate limiting

# Save updated results
with open('data/wiki_portraits_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

local_count = sum(1 for v in results.values() if v.startswith('data/'))
remaining_final = [k for k, v in results.items() if not v.startswith('data/')]
print(f'\nFinal: {local_count} local portraits ready')
print(f'Still missing: {remaining_final}')
