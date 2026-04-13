import json, re

with open('data/philosophers.json', 'r', encoding='utf-8') as f:
    western = json.load(f)
with open('data/chinese-philosophers.json', 'r', encoding='utf-8') as f:
    chinese = json.load(f)

with open('js/i18n-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract name section
name_start = content.index("  name: {")
name_end = content.index('  },', name_start + 10)
name_section = content[name_start:name_end]
existing_names = set(re.findall(r"'([^']+)'\s*:", name_section))

all_phil_ids = set()
for p in western + chinese:
    all_phil_ids.add(p['id'])

missing_names = all_phil_ids - existing_names
print(f"Total philosophers: {len(all_phil_ids)}")
print(f"In i18n-data.js names: {len(existing_names)}")
print(f"Missing names: {len(missing_names)}")
if missing_names:
    for mid in sorted(missing_names):
        for p in western + chinese:
            if p['id'] == mid:
                safe_name = p['name'].encode('ascii', 'replace').decode('ascii')
                print(f"  {mid}: {safe_name}")
