import json, re

with open('data/connections.json', 'r', encoding='utf-8') as f:
    western_conns = json.load(f)
with open('data/chinese-connections.json', 'r', encoding='utf-8') as f:
    chinese_conns = json.load(f)

with open('js/i18n-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

conn_start = content.index("  conn: {")
conn_end = content.index('  },', conn_start + 10)
conn_section = content[conn_start:conn_end]

# Find all conn entries that have en == zh (these are the fallbacks)
import re as re2
entries = re2.findall(r"'([^']+)':\s*\{\s*en:\s*'([^']+)',\s*zh:\s*'([^']+)'\s*\}", conn_section)

same_count = 0
diff_count = 0
same_entries = []
for key, en, zh in entries:
    if en == zh:
        same_count += 1
        same_entries.append(key)
    else:
        diff_count += 1

print(f"Total conn entries: {len(entries)}")
print(f"en == zh (need translation): {same_count}")
print(f"en != zh (already translated): {diff_count}")
print(f"\nSample untranslated ({len(same_entries)} total):")
for s in same_entries[:10]:
    print(f"  {s}")
