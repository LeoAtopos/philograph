import json
import re

# Load connections
with open('data/connections.json', 'r', encoding='utf-8') as f:
    western_conns = json.load(f)
with open('data/chinese-connections.json', 'r', encoding='utf-8') as f:
    chinese_conns = json.load(f)

# Parse i18n-data.js
with open('js/i18n-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

conn_start = content.index("  conn: {")
conn_end = content.index('  },', conn_start + 10)
conn_section = content[conn_start:conn_end]
existing_conn_ids = set(re.findall(r"'([^']+)':\s*\{", conn_section))

# Collect all conn keys
all_conn_keys = set()
for c in western_conns + chinese_conns:
    key = f"{c['from']}-{c['to']}"
    all_conn_keys.add(key)

missing_conn = sorted(all_conn_keys - existing_conn_ids)
print(f"Total conn keys: {len(all_conn_keys)}")
print(f"Existing: {len(existing_conn_ids)}")
print(f"Missing: {len(missing_conn)}")
if missing_conn:
    for mk in missing_conn[:20]:
        print(f"  {mk}")
    if len(missing_conn) > 20:
        print(f"  ... and {len(missing_conn)-20} more")
