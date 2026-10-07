"""Record deterministic table classifications after a validated source change."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/table-dispositions.json'
data=json.loads(path.read_text())
snapshot=json.loads((ROOT/'site/assets/reference-data.json').read_text())
fields=('id','article_id','path','disposition','classification_basis','review','rows','tool')
data['tables']=[{k:row.get(k) for k in fields} for row in snapshot['tables']]
path.write_text(json.dumps(data,indent=2)+'\n')
