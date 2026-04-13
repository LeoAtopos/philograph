import json
phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
target_ids = ['hobbes','schopenhauer','kierkegaard','peirce','husserl','heidegger',
              'ockham','montesquieu','weber','nozick','davidson','searle','singer']
for p in phil:
    if p['id'] in target_ids:
        ids = [i['id'] for i in p['ideas']]
        print(f"{p['id']}: {ids}")
    elif p['id'] not in ('ockham','montesquieu','weber','nozick','davidson','searle','singer'):
        pass  # skip
