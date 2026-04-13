import json, re

with open('data/philosophers.json', 'r', encoding='utf-8') as f:
    western = json.load(f)
with open('data/chinese-philosophers.json', 'r', encoding='utf-8') as f:
    chinese = json.load(f)

with open('js/i18n-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

idea_start = content.index("  idea: {")
idea_end = content.index('  },', idea_start + 10)
idea_section = content[idea_start:idea_end]
existing_ids = set(re.findall(r"'([a-z]+\d+)'\s*:", idea_section))

all_ids = set()
for p in western + chinese:
    for idea in p['ideas']:
        all_ids.add(idea['id'])

missing = all_ids - existing_ids
print(f"Total ideas: {len(all_ids)}")
print(f"In i18n-data.js: {len(existing_ids)}")
print(f"Still missing: {len(missing)}")
