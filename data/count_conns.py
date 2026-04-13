import json
phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
conn = json.load(open('connections.json', 'r', encoding='utf-8'))

# Count connections per philosopher
conn_count = {}
for c in conn:
    conn_count[c['fromPhil']] = conn_count.get(c['fromPhil'], 0) + 1
    conn_count[c['toPhil']] = conn_count.get(c['toPhil'], 0) + 1

# List all philosophers with their connection counts
for p in sorted(phil, key=lambda x: x['born']):
    pid = p['id']
    n_conn = conn_count.get(pid, 0)
    n_ideas = len(p['ideas'])
    marker = " *** NO CONNS" if n_conn == 0 else ""
    print(f"{pid:20s}  ideas={n_ideas}  conns={n_conn}{marker}")
