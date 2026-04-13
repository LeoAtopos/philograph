import json

phil = json.load(open('philosophers.json', 'r', encoding='utf-8'))
conn = json.load(open('connections.json', 'r', encoding='utf-8'))

# Remove 8 philosophers to get to exactly 50
# Criteria: no connections + relatively less central to the core narrative
# Keep: heraclitus, parmenides (pre-Socratic foundations)
# Remove: democritus, cicero, avicenna, averroes, maimonides, bentham, comte, weber
# Actually, let me reconsider - these are all important philosophers
# But we need 50. Let me remove the 8 with 0 connections (except keep heraclitus, parmenides)
# and then we'd need to remove 1 more from the connected ones

remove_ids = [
    'democritus',    # 0 conns - important but less central than atomism in Epicurus
    'cicero',        # 0 conns - important Roman but less philosophically original
    'avicenna',      # 0 conns - important Islamic philosopher, but no connections
    'averroes',      # 0 conns - important commentator, but no connections  
    'maimonides',    # 0 conns - important Jewish philosopher, but no connections
    'bentham',       # 0 conns - utilitarianism is represented by Mill
    'comte',         # 0 conns - positivism, less central
    'weber',         # 2 conns - sociology, important but less central to philosophy
]

remaining = [p for p in phil if p['id'] not in remove_ids]
print(f"Removed {len(remove_ids)} philosophers. Remaining: {len(remaining)}")

# Verify no connections reference removed philosophers
removed_set = set(remove_ids)
for c in conn:
    if c['fromPhil'] in removed_set or c['toPhil'] in removed_set:
        print(f"  WARNING: connection references removed philosopher: {c['fromPhil']} -> {c['toPhil']}")

# Sort by birth year
remaining.sort(key=lambda x: x['born'])

# Save
with open('philosophers.json', 'w', encoding='utf-8') as f:
    json.dump(remaining, f, ensure_ascii=False, indent=2)

print(f"Written {len(remaining)} philosophers to philosophers.json")
