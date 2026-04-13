import json

chinese_phil = json.load(open('chinese-philosophers.json', 'r', encoding='utf-8'))
chinese_conn = json.load(open('chinese-connections.json', 'r', encoding='utf-8'))

# Build idea ID map
idea_ids = {}
for p in chinese_phil:
    for i in p['ideas']:
        idea_ids[i['id']] = p['id']

print(f"Chinese philosophers: {len(chinese_phil)}")
print(f"Total idea IDs: {len(idea_ids)}")
print(f"Total connections: {len(chinese_conn)}")

# Verify all connections
broken = 0
for c in chinese_conn:
    if c['from'] not in idea_ids:
        print(f"  BROKEN: {c['from']} (phil: {c['fromPhil']})")
        broken += 1
    if c['to'] not in idea_ids:
        print(f"  BROKEN: {c['to']} (phil: {c['toPhil']})")
        broken += 1

if broken == 0:
    print("ALL CHINESE CONNECTIONS VERIFIED!")

# Count connections per philosopher
from collections import Counter
conn_count = Counter()
for c in chinese_conn:
    conn_count[c['fromPhil']] += 1
    conn_count[c['toPhil']] += 1

# Check which philosophers have no connections
all_ids = {p['id'] for p in chinese_phil}
no_conns = all_ids - set(conn_count.keys())
if no_conns:
    print(f"\nPhilosophers with no connections: {no_conns}")

# Also check that build script references are correct (e.g., ar10, ar12, xz6)
cross_refs = [(c['fromPhil'], c['toPhil']) for c in chinese_conn]
western_ids = set()
for pair in cross_refs:
    for pid in pair:
        if pid not in all_ids:
            western_ids.add(pid)

if western_ids:
    print(f"\nNote: {len(western_ids)} Western philosophers referenced in Chinese connections: {western_ids}")
    
    # Check if these exist in philosophers.json
    western_phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
    western_ids_set = {p['id'] for p in western_phil}
    missing = western_ids - western_ids_set
    if missing:
        print(f"  MISSING from western philosophers.json: {missing}")
    else:
        print(f"  All Western references exist in philosophers.json")
