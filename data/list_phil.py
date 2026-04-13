import json
phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
print(f"Total: {len(phil)}")
for p in sorted(phil, key=lambda x: x['born']):
    n = len(p['ideas'])
    print(f"{p['id']:20s} born={str(p['born']):>6s}  {p['era']:20s}  ideas={n}")
