import json
import re

with open('data/connections.json', 'r', encoding='utf-8') as f:
    western_conns = json.load(f)
with open('data/chinese-connections.json', 'r', encoding='utf-8') as f:
    chinese_conns = json.load(f)

with open('js/i18n-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

conn_start = content.index("  conn: {")
conn_end = content.index('  },', conn_start + 10)
conn_section = content[conn_start:conn_end]
existing_conn_ids = set(re.findall(r"'([^']+)':\s*\{", conn_section))

all_conn_keys = set()
for c in western_conns + chinese_conns:
    key = f"{c['from']}-{c['to']}"
    all_conn_keys.add(key)

missing_conn = {k: v for k, v in {f"{c['from']}-{c['to']}": c for c in western_conns + chinese_conns}.items() if k not in existing_conn_ids}

# Check sample keys
print("Sample missing conn keys:", sorted(missing_conn.keys())[:10])
# Check if ZH_CONN has these keys
test_keys = ['ag3-sc6', 'ag5-pl3', 'an1-hg7']
# The issue is likely that some conn keys in data have different formats
# Let me check the actual keys
all_keys = set()
for c in western_conns + chinese_conns:
    all_keys.add(f"{c['from']}-{c['to']}")

# Check which are missing and should be in ZH_CONN
zh_keys_sample = ['ag3-sc6', 'ag5-pl3', 'an1-hg7', 'cy4-xz1', 'ch2-kz1']
for k in zh_keys_sample:
    in_all = k in all_keys
    in_existing = k in existing_conn_ids
    print(f"  {k}: in_all={in_all}, in_existing={in_existing}, is_missing={in_all and not in_existing}")
