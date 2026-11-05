#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import json,sys
root=Path(__file__).resolve().parents[1];assets=root/'app/src/main/assets';data=json.loads((assets/'pets.json').read_text());errors=[];ids=set()
if not data:errors.append('Empty catalog')
for entry in data:
 try:
  ident=entry['id'];file=entry['file'];fw=entry['frameWidth'];fh=entry['frameHeight']
  assert ident not in ids,'Duplicate id';ids.add(ident)
  assert not Path(file).is_absolute() and '..' not in Path(file).parts,'Unsafe file path'
  im=Image.open(assets/file);assert fw>0 and fh>0 and im.width%fw==0 and im.height==fh,'Invalid frame grid'
  assert 0<entry.get('fps',8)<=60,'Invalid fps'
  assert not (entry.get('eyes') or entry.get('accessories')) or (fw,fh)==(32,32),'Built-in masks require 32x32'
  assert im.mode=='RGBA' and im.getextrema()[3][0]==0,'Expected transparent RGBA'
  print(f"PASS {ident}: {im.width//fw} frames, {fw}x{fh}, {entry.get('fps',8)} fps")
 except (KeyError,AssertionError,OSError,TypeError) as exc:errors.append(f"{entry.get('id','?')}: {exc}")
if errors:
 print('\n'.join(errors),file=sys.stderr);sys.exit(1)
print(f'PASS catalog: {len(data)} characters')
