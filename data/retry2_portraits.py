"""Final retry for remaining 5 philosophers."""
import urllib.request
import urllib.parse
import json
import os
import time
import ssl

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'portraits')

# Try multiple search titles and languages
SEARCHES = [
    ("kuhn", [("Thomas_Kuhn", "en"), ("Thomas_S._Kuhn", "en"), ("Thomas_Kuhn", "zh")]),
    ("zhuangzi", [("Zhuang_Zhou", "en"), ("Zhuangzi", "en"), ("庄子", "zh")]),
    ("xunzi", [("Xun_Kuang", "en"), ("Xunzi", "en"), ("荀子", "zh")]),
    ("wangchong", [("Wang_Chong", "en"), ("王充", "zh")]),
    ("han_yu", [("Han_Yu", "en"), ("韩愈", "zh"), ("Han_Yu_(Tang_dynasty)", "en")]),
]

def get_page_image_url(title, lang='en'):
    params = urllib.parse.urlencode({
        'action': 'query',
        'titles': title,
        'prop': 'pageimages',
        'pithumbsize': 200,
        'format': 'json',
    })
    url = f'https://{lang}.wikipedia.org/w/api.php?{params}'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Philograph/1.0 (philosophy visualization project)'})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  API error: {e}")
        return None
    pages = data.get('query', {}).get('pages', {})
    for pid, pdata in pages.items():
        if int(pid) > 0 and 'thumbnail' in pdata:
            return pdata['thumbnail']['source']
    return None

def download_image(url, filepath):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Philograph/1.0 (philosophy visualization project)'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            with open(filepath, 'wb') as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download error: {e}")
        return False

results = {}
for local_id, attempts in SEARCHES:
    found = False
    for title, lang in attempts:
        print(f"  Trying {local_id}: {title} ({lang})...")
        img_url = get_page_image_url(title, lang)
        if img_url:
            ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1] or '.jpg'
            filepath = os.path.join(OUTPUT_DIR, f"{local_id}{ext}")
            if download_image(img_url, filepath):
                results[local_id] = f"data/portraits/{local_id}{ext}"
                print(f"[OK] {local_id:20s} -> {local_id}{ext}")
                found = True
                break
            else:
                print(f"[FAIL] {local_id} download failed for {title}")
        time.sleep(2)
    if not found:
        print(f"[NONE] {local_id:20s} no image found")

print(f"\n=== Results ===")
for k, v in sorted(results.items()):
    print(f'  "{k}": "{v}",')
