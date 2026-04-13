import json
conn = json.load(open('connections.json', 'r', encoding='utf-8'))
conn = [c for c in conn if c['fromPhil'] != 'averroes' and c['toPhil'] != 'averroes']
with open('connections.json', 'w', encoding='utf-8') as f:
    json.dump(conn, f, ensure_ascii=False, indent=2)

# Verify
phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
idea_ids = {}
for p in phil:
    for i in p['ideas']:
        idea_ids[i['id']] = p['id']

broken = 0
for c in conn:
    if c['from'] not in idea_ids:
        print(f"BROKEN: {c['from']} (phil: {c['fromPhil']})")
        broken += 1
    if c['to'] not in idea_ids:
        print(f"BROKEN: {c['to']} (phil: {c['toPhil']})")
        broken += 1

print(f"Connections: {len(conn)}, Broken: {broken}")
if broken == 0:
    print("ALL VERIFIED!")
