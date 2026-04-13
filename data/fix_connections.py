"""
Fix connections.json ID references and add missing philosophers.
This script:
1. Fixes broken idea ID references in connections.json (wrong prefixes)
2. Adds 7 missing philosophers to philosophers.json (ockham, montesquieu, weber, nozick, davidson, searle, singer)
3. Verifies all connections are valid after fixes
"""
import json

# Load data
phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
conn = json.load(open('connections.json', 'r', encoding='utf-8'))

# === Step 1: Build idea ID map ===
idea_ids = {}
for p in phil:
    for i in p['ideas']:
        idea_ids[i['id']] = p['id']

# === Step 2: Define ID remapping for connections with wrong prefixes ===
id_remap = {
    # Schopenhauer: so -> sh
    'so1': 'sh1', 'so2': 'sh2',
    # Hobbes: ho -> hb
    'ho1': 'hb1', 'ho2': 'hb2', 'ho3': 'hb3', 'ho4': 'hb4',
    # Kierkegaard: kg -> kk
    'kg1': 'kk1', 'kg2': 'kk2', 'kg3': 'kk3', 'kg4': 'kk4', 'kg5': 'kk5', 'kg6': 'kk6',
    # Peirce: pr -> pc
    'pr1': 'pc1', 'pr2': 'pc2', 'pr3': 'pc3', 'pr4': 'pc4', 'pr5': 'pc5',
    # Husserl: hu -> hs
    'hu1': 'hs1', 'hu2': 'hs2', 'hu3': 'hs3', 'hu4': 'hs4', 'hu5': 'hs5', 'hu6': 'hs6',
    # Heidegger: hd -> he
    'hd1': 'he1', 'hd2': 'he2', 'hd3': 'he3', 'hd4': 'he4', 'hd5': 'he5',
    'hd6': 'he6', 'hd7': 'he7', 'hd8': 'he8',
    # Comte: cm -> co (if needed)
    'cm1': 'co1', 'cm2': 'co2', 'cm3': 'co3', 'cm4': 'co4',
}

# Apply remapping to connections
fixes_count = 0
for c in conn:
    if c['from'] in id_remap:
        old = c['from']
        c['from'] = id_remap[old]
        fixes_count += 1
    if c['to'] in id_remap:
        old = c['to']
        c['to'] = id_remap[old]
        fixes_count += 1

print(f"Applied {fixes_count} ID remappings")

# === Step 3: Add missing philosophers ===
# Determine which are still missing after remapping
missing_phils = set()
missing_idea_ids = set()
for c in conn:
    if c['from'] not in idea_ids:
        missing_phils.add(c['fromPhil'])
        missing_idea_ids.add(c['from'])
    if c['to'] not in idea_ids:
        missing_phils.add(c['toPhil'])
        missing_idea_ids.add(c['to'])

print(f"Still missing philosophers: {missing_phils}")
print(f"Still missing idea IDs: {missing_idea_ids}")

# Add the 7 missing philosophers
new_philosophers = [
    {
        "id": "ockham",
        "name": "William of Ockham",
        "born": 1285,
        "died": 1349,
        "era": "Medieval",
        "portrait": "https://placehold.co/60x60/1a1a20/C0A080?text=WO",
        "tags": ["Logic", "Epistemology", "Metaphysics"],
        "ideas": [
            {"id": "ok1", "text": "Ockham's Razor: do not multiply entities beyond necessity — simpler explanations are preferred", "tags": ["Logic", "Epistemology"]},
            {"id": "ok2", "text": "Nominalism: universals are names (flatus vocis), not real entities existing independently", "tags": ["Metaphysics", "Language"]},
            {"id": "ok3", "text": "Only individuals exist; all categories are mental constructs for organizing experience", "tags": ["Metaphysics", "Epistemology"]},
            {"id": "ok4", "text": "Faith and reason are separate domains — theological truths cannot be proven by reason alone", "tags": ["Religion", "Epistemology"]}
        ]
    },
    {
        "id": "montesquieu",
        "name": "Montesquieu",
        "born": 1689,
        "died": 1755,
        "era": "Enlightenment",
        "portrait": "https://placehold.co/60x60/1a2030/B08080?text=MQ",
        "tags": ["Political", "Ethics"],
        "ideas": [
            {"id": "mq1", "text": "Separation of powers (executive, legislative, judicial) is essential to prevent tyranny", "tags": ["Political"]},
            {"id": "mq2", "text": "Laws must be adapted to the people, climate, and customs of each nation — legal relativism", "tags": ["Political", "Ethics"]},
            {"id": "mq3", "text": "Despotism is ruled by fear; monarchy by honor; republic by virtue", "tags": ["Political"]},
            {"id": "mq4", "text": "Commerce promotes peace and tolerance between nations", "tags": ["Political", "Ethics"]}
        ]
    },
    {
        "id": "weber",
        "name": "Max Weber",
        "born": 1864,
        "died": 1920,
        "era": "20th Century",
        "portrait": "https://placehold.co/60x60/1a1a2a/A0A0B0?text=MW",
        "tags": ["Political", "Epistemology", "Ethics"],
        "ideas": [
            {"id": "wb1", "text": "Verstehen (interpretive understanding): social science requires empathetic interpretation, not just causal explanation", "tags": ["Epistemology"]},
            {"id": "wb2", "text": "The Protestant Ethic: Calvinist theology unintentionally fostered modern capitalism", "tags": ["Political", "Religion"]},
            {"id": "wb3", "text": "Rationalization: modern society is increasingly dominated by bureaucratic efficiency and calculability", "tags": ["Political", "Ethics"]},
            {"id": "wb4", "text": "Value-freedom (Wertfreiheit): scholars should separate empirical analysis from moral judgment", "tags": ["Epistemology", "Ethics"]}
        ]
    },
    {
        "id": "nozick",
        "name": "Robert Nozick",
        "born": 1938,
        "died": 2002,
        "era": "Analytic",
        "portrait": "https://placehold.co/60x60/1a1a2a/80A0C0?text=RN",
        "tags": ["Political", "Ethics"],
        "ideas": [
            {"id": "nz1", "text": "The minimal state: only functions needed to protect against force, theft, fraud, and enforce contracts", "tags": ["Political"]},
            {"id": "nz2", "text": "Entitlement theory: justice in holdings depends on just acquisition and voluntary transfer", "tags": ["Political", "Ethics"]},
            {"id": "nz3", "text": "Taxation of earnings from labor is on a par with forced labor", "tags": ["Political", "Ethics"]},
            {"id": "nz4", "text": "The Utility Monster: if a being gets enormously more utility from resources, utilitarianism would sacrifice everyone else", "tags": ["Ethics"]}
        ]
    },
    {
        "id": "davidson",
        "name": "Donald Davidson",
        "born": 1917,
        "died": 2003,
        "era": "Analytic",
        "portrait": "https://placehold.co/60x60/1a2020/B0A080?text=DD",
        "tags": ["Mind", "Language", "Epistemology"],
        "ideas": [
            {"id": "dv1", "text": "Anomalous monism: mental events are identical with physical events but have no strict psychophysical laws", "tags": ["Mind", "Metaphysics"]},
            {"id": "dv2", "text": "Principle of charity: we must assume most of a speaker's beliefs are true to interpret them at all", "tags": ["Language", "Epistemology"]},
            {"id": "dv3", "text": "Triangulation: thought, language, and knowledge require interaction between two creatures and a shared world", "tags": ["Mind", "Epistemology"]},
            {"id": "dv4", "text": "Radical interpretation: understanding a language requires simultaneously interpreting beliefs and meanings", "tags": ["Language", "Epistemology"]}
        ]
    },
    {
        "id": "searle",
        "name": "John Searle",
        "born": 1932,
        "died": 2024,
        "era": "Analytic",
        "portrait": "https://placehold.co/60x60/202020/A0B0A0?text=JS",
        "tags": ["Mind", "Language", "Epistemology"],
        "ideas": [
            {"id": "sr1", "text": "The Chinese Room: syntax manipulation is not sufficient for semantics — computation is not understanding", "tags": ["Mind", "Epistemology"]},
            {"id": "sr2", "text": "Speech acts: language is not just describing reality but performing actions (asserting, promising, commanding)", "tags": ["Language"]},
            {"id": "sr3", "text": "Biological naturalism: consciousness is a biological phenomenon caused by brain processes", "tags": ["Mind"]},
            {"id": "sr4", "text": "Social reality: institutional facts (money, marriage, property) depend on collective intentionality", "tags": ["Mind", "Political"]}
        ]
    },
    {
        "id": "singer",
        "name": "Peter Singer",
        "born": 1946,
        "era": "Contemporary",
        "portrait": "https://placehold.co/60x60/101a30/B0C080?text=PS",
        "tags": ["Ethics", "Political"],
        "ideas": [
            {"id": "sg1", "text": "All sentient beings deserve equal consideration of interests — speciesism is morally wrong", "tags": ["Ethics"]},
            {"id": "sg2", "text": "Preference utilitarianism: maximize the satisfaction of preferences of all affected beings", "tags": ["Ethics"]},
            {"id": "sg3", "text": "Effective altruism: we should donate to causes that do the most good per dollar spent", "tags": ["Ethics", "Political"]},
            {"id": "sg4", "text": "Famine, Affluence, and Morality: if we can prevent suffering without sacrificing anything comparable, we must", "tags": ["Ethics"]}
        ]
    }
]

# Add new philosophers to the list
for np in new_philosophers:
    # Insert in chronological order
    phil.append(np)
    
# Now sort by born date
phil.sort(key=lambda p: p['born'])

print(f"Added {len(new_philosophers)} philosophers. Total: {len(phil)}")

# === Step 4: Verify all connections are valid ===
idea_ids = {}
for p in phil:
    for i in p['ideas']:
        idea_ids[i['id']] = p['id']

broken = 0
for c in conn:
    if c['from'] not in idea_ids:
        print(f"  STILL BROKEN: {c['from']} (phil: {c['fromPhil']})")
        broken += 1
    if c['to'] not in idea_ids:
        print(f"  STILL BROKEN: {c['to']} (phil: {c['toPhil']})")
        broken += 1

if broken == 0:
    print("All connections verified successfully!")
else:
    print(f"{broken} broken connections remain")

# === Step 5: Write output files ===
with open('philosophers.json', 'w', encoding='utf-8') as f:
    json.dump(phil, f, ensure_ascii=False, indent=2)

with open('connections.json', 'w', encoding='utf-8') as f:
    json.dump(conn, f, ensure_ascii=False, indent=2)

print(f"\nFinal Western philosophers: {len(phil)}")
print(f"Total connections: {len(conn)}")
print("Written to philosophers.json and connections.json")
