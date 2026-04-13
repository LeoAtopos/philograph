import json

with open('data/chinese-philosophers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data:
    if p['id'] == 'zhangzai':
        p['portrait'] = 'data/portraits/zhangzai.jpg'
        print(f"Updated zhangzai: {p['portrait']}")
        break

with open('data/chinese-philosophers.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
