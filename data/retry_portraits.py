"""Retry downloading failed portraits and clean up bad ones."""
import json
import urllib.request
import os
import time
import ssl

portraits_dir = os.path.join('data', 'portraits')
os.makedirs(portraits_dir, exist_ok=True)

with open('data/wiki_portraits_result.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

ctx = ssl.create_default_context()

# Retry downloads for entries that still have wikimedia URLs
for phil_id, url in list(results.items()):
    if 'wikimedia' in url and not url.startswith('data/'):
        print(f'  Retrying {phil_id}...', end=' ', flush=True)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'PhilographBot/1.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                data = resp.read()
                ext = os.path.splitext(url.split('?')[0])[1] or '.jpg'
                if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
                    ext = '.jpg'
                local_path = os.path.join(portraits_dir, f'{phil_id}{ext}')
                with open(local_path, 'wb') as f:
                    f.write(data)
                results[phil_id] = f'data/portraits/{phil_id}{ext}'
                print(f'OK -> {phil_id}{ext} ({len(data)} bytes)')
        except Exception as e:
            print(f'FAILED: {e}')
        time.sleep(2)

# Handle parmenides timeout
if 'parmenides' in results and 'wikimedia' in results.get('parmenides', ''):
    print('  Retrying parmenides...', end=' ', flush=True)
    try:
        req = urllib.request.Request(results['parmenides'], headers={'User-Agent': 'PhilographBot/1.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()
            local_path = os.path.join(portraits_dir, 'parmenides.jpg')
            with open(local_path, 'wb') as f:
                f.write(data)
            results['parmenides'] = 'data/portraits/parmenides.jpg'
            print(f'OK -> parmenides.jpg ({len(data)} bytes)')
    except Exception as e:
        print(f'FAILED: {e}')

# Remove bad images (PDFs, group photos, calligraphy)
for bad_id in ['shen_buhai', 'jikang', 'liezi']:
    if bad_id in results:
        print(f'  Removing bad image for {bad_id} (not a proper portrait)')
        del results[bad_id]

with open('data/wiki_portraits_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Summary
local_count = sum(1 for v in results.values() if v.startswith('data/'))
remaining = [k for k, v in results.items() if not v.startswith('data/')]
print(f'\nFinal: {local_count} local portraits ready')
print(f'Remaining URLs (not downloaded): {remaining}')
