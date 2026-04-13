import json
conn = json.load(open('connections.json', 'r', encoding='utf-8'))

# Fix Pascal: pa -> ps
pascal_remap = {'pa1': 'ps1', 'pa2': 'ps2', 'pa3': 'ps3', 'pa4': 'ps4'}
count = 0
for c in conn:
    if c['from'] in pascal_remap:
        c['from'] = pascal_remap[c['from']]
        count += 1
    if c['to'] in pascal_remap:
        c['to'] = pascal_remap[c['to']]
        count += 1

print(f"Fixed {count} Pascal ID references")

# Verify
phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
idea_ids = {}
for p in phil:
    for i in p['ideas']:
        idea_ids[i['id']] = p['id']

broken = 0
for c in conn:
    if c['from'] not in idea_ids:
        print(f"  BROKEN: {c['from']} (phil: {c['fromPhil']})")
        broken += 1
    if c['to'] not in idea_ids:
        print(f"  BROKEN: {c['to']} (phil: {c['toPhil']})")
        broken += 1

if broken == 0:
    print("ALL CONNECTIONS VERIFIED!")

with open('connections.json', 'w', encoding='utf-8') as f:
    json.dump(conn, f, ensure_ascii=False, indent=2)
