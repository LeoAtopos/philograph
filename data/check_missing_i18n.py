import json
import re

# Load philosophers
with open('data/philosophers.json', 'r', encoding='utf-8') as f:
    western = json.load(f)
with open('data/chinese-philosophers.json', 'r', encoding='utf-8') as f:
    chinese = json.load(f)

# Collect all idea IDs
all_ids = set()
for p in western:
    for idea in p['ideas']:
        all_ids.add(idea['id'])
for p in chinese:
    for idea in p['ideas']:
        all_ids.add(idea['id'])

# Parse i18n-data.js to get idea IDs in translation
with open('js/i18n-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find idea section
idea_start = content.index("  idea: {")
idea_end = content.index('  },', idea_start + 10)
idea_section = content[idea_start:idea_end]

# Extract all keys
translated_ids = set(re.findall(r"'([a-z]+\d+)'\s*:\s*\{", idea_section))

missing = sorted(all_ids - translated_ids)
print(f'Total idea IDs in data: {len(all_ids)}')
print(f'Total idea IDs in translation: {len(translated_ids)}')
print(f'Missing translations ({len(missing)}):')
for mid in missing:
    for p in western + chinese:
        for idea in p['ideas']:
            if idea['id'] == mid:
                text_safe = idea["text"][:80].encode('ascii', 'replace').decode('ascii')
                name_safe = p["name"].encode('ascii', 'replace').decode('ascii')
                print(f'  {mid} -> {name_safe}: {text_safe}...')
                break
