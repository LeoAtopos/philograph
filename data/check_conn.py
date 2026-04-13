import json

phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
conn = json.load(open('connections.json', 'r', encoding='utf-8'))

# Get all existing idea IDs
idea_ids = {}
for p in phil:
    for i in p['ideas']:
        idea_ids[i['id']] = p['id']

# For each connection, check if both sides exist
for c in conn:
    f = c['from']
    t = c['to']
    if f not in idea_ids or t not in idea_ids:
        f_phil = c['fromPhil']
        t_phil = c['toPhil']
        f_ok = "OK" if f in idea_ids else "MISSING"
        t_ok = "OK" if t in idea_ids else "MISSING"
        print(f"{f}({f_phil})[{f_ok}] -> {t}({t_phil})[{t_ok}]")
