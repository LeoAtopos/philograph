import json
conn = json.load(open('connections.json', 'r', encoding='utf-8'))

removed = {'democritus', 'cicero', 'avicenna', 'averroes', 'maimonides', 'bentham', 'comte', 'weber'}
before = len(conn)
conn = [c for c in conn if c['fromPhil'] not in removed and c['toPhil'] not in removed]
after = len(conn)

with open('connections.json', 'w', encoding='utf-8') as f:
    json.dump(conn, f, ensure_ascii=False, indent=2)

print(f"Removed {before - after} connections. Remaining: {after}")

# Final verification
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
