"""
Update philosopher JSON files with new portrait paths from Wikipedia.
Only updates portrait field for philosophers that got new images.
"""
import json
import os

# Load portrait results
with open(os.path.join('data', 'wiki_portraits_result.json'), 'r', encoding='utf-8') as f:
    portraits = json.load(f)

# Filter only local portrait paths
local_portraits = {k: v for k, v in portraits.items() if v.startswith('data/portraits/')}
print(f"Local portraits to apply: {len(local_portraits)}")

# --- Update Western philosophers ---
with open(os.path.join('data', 'philosophers.json'), 'r', encoding='utf-8') as f:
    western = json.load(f)

updated_western = 0
for phil in western:
    pid = phil['id']
    if pid in local_portraits:
        old = phil['portrait']
        new = local_portraits[pid]
        if old != new:
            phil['portrait'] = new
            updated_western += 1
            print(f"  [Western] {phil['name']}: {old[:40]}... -> {new}")

with open(os.path.join('data', 'philosophers.json'), 'w', encoding='utf-8') as f:
    json.dump(western, f, indent=2, ensure_ascii=False)

print(f"\nUpdated {updated_western} western philosophers")

# --- Update Chinese philosophers ---
with open(os.path.join('data', 'chinese-philosophers.json'), 'r', encoding='utf-8') as f:
    chinese = json.load(f)

updated_chinese = 0
for phil in chinese:
    pid = phil['id']
    if pid in local_portraits:
        old = phil['portrait']
        new = local_portraits[pid]
        if old != new:
            phil['portrait'] = new
            updated_chinese += 1
            print(f"  [Chinese] {phil['name']}: '{old}' -> '{new}'")

with open(os.path.join('data', 'chinese-philosophers.json'), 'w', encoding='utf-8') as f:
    json.dump(chinese, f, indent=2, ensure_ascii=False)

print(f"\nUpdated {updated_chinese} chinese philosophers")

# --- Summary ---
print(f"\nTotal: {updated_western + updated_chinese} portrait paths updated")

# List philosophers still without real portraits
still_missing_western = [p['name'] for p in western if p['portrait'].startswith('https://placehold.co')]
still_missing_chinese = [p['name'] for p in chinese if not p['portrait']]
print(f"\nStill missing portraits:")
print(f"  Western ({len(still_missing_western)}): {', '.join(still_missing_western) if still_missing_western else 'None'}")
print(f"  Chinese ({len(still_missing_chinese)}): {', '.join(still_missing_chinese) if still_missing_chinese else 'None'}")
