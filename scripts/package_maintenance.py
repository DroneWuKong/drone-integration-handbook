"""Package only public maintenance changes for a separate validation job."""
import argparse
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PUBLIC_DATA={'data/evidence.json','data/table-dispositions.json','data/update-status.json','data/emerging-watch.json'}
CONTENT={'fundamentals','firmware','field','integration','components','platforms','autonomy','appendices'}
def package(output,include_tables=False):
    output=(ROOT/output).resolve()
    if output.parent!=ROOT/'.local' or not output.name.startswith('maintenance-'):
        raise ValueError('Output must be a maintenance staging directory')
    paths=json.loads((ROOT/'.local/autonomy/changed-files.json').read_text())
    if include_tables:paths.append('data/table-dispositions.json')
    files=[]
    for value in sorted(set(paths)):
        path=Path(value);source=ROOT/path
        if path.is_absolute() or '..' in path.parts or not path.parts:
            raise ValueError('Invalid publication path')
        if not (value in PUBLIC_DATA or (path.parts[0] in CONTENT and path.suffix=='.md')):
            raise ValueError('Nonpublic artifact rejected')
        if source.resolve()!=source.absolute() or not source.is_file():
            raise ValueError('Symlink or missing source rejected')
        files.append(path)
    if output.exists():shutil.rmtree(output)
    output.mkdir(parents=True)
    for path in files:
        target=output/path;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/path,target)
    manifest=output/'.local/autonomy/changed-files.json'
    manifest.parent.mkdir(parents=True,exist_ok=True)
    manifest.write_text(json.dumps([p.as_posix() for p in files],indent=2)+'\n')
    return len(files)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--include-tables',action='store_true')
    args=parser.parse_args();print(json.dumps({'public_files':package(args.output,args.include_tables)}))
