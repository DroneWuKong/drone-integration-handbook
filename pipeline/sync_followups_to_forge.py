"""Sync followup flags from handbook to Forge pie_flags.json with proper schema mapping"""
import json, sys

FORGE_PIE = sys.argv[1] if len(sys.argv) > 1 else "pie_flags.json"
HANDBOOK_FOLLOWUPS = sys.argv[2] if len(sys.argv) > 2 else "followup_flags.json"

with open(FORGE_PIE) as f:
    flags = json.load(f)
fl = flags if isinstance(flags, list) else flags.get('flags', [])

# Remove old followups
fl = [f for f in fl if not f.get('id','').startswith('gz-followup')]

with open(HANDBOOK_FOLLOWUPS) as f:
    followups = json.load(f)

for ff in followups:
    cat = ff.get('category', 'research')
    sev = ff.get('severity', 'info').lower()
    if sev == 'high': sev = 'warning'
    
    fl.append({
        'id': ff['id'],
        'title': ff['title'],
        'flag_type': 'grayzone' if 'market' not in cat else 'contract_signal',
        'timestamp': ff.get('date', '2026-04-04'),
        'severity': sev,
        'confidence': 0.90,
        'detail': ff.get('detail', ''),
        'source_urls': ff.get('sources', []),
        'category': f"gray_zone_{cat}",
    })

output = fl if isinstance(flags, list) else {**flags, 'flags': fl}
with open(FORGE_PIE, 'w') as f:
    json.dump(output, f, indent=2)

print(f"Synced {len(followups)} followup flags. Total: {len(fl)}")
