#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import json,hashlib,zipfile
r=Path(__file__).resolve().parents[1];files=[];known={'Idle.png':(32,32),'drculacat.png':(32,32),'Box3.png':(32,32),'EvilBox1.png':(32,32),'WitchFlying.png':(48,64),'VampireAngry.png':(32,32)}
for p in sorted((r/'original').glob('*.png')):
 if '.preview.' not in p.name:files.append((p,'CatPackFree/'+p.name,'CatPackFree.zip'))
for p in sorted((r/'extra-packs').rglob('*')):
 if p.is_file():files.append((p,str(p.relative_to(r/'extra-packs')),p.relative_to(r/'extra-packs').parts[0]+'.zip'))
index=[]
for path,archive,source in files:
 row={'path':archive,'sourceArchive':source,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'license':'not supplied; see ORIGEM-E-LICENCAS.md'}
 if path.suffix.lower()=='.png':
  im=Image.open(path);row['width'],row['height']=im.size;row['mode']=im.mode
  if path.name in known:
   fw,fh=known[path.name];row.update(kind='character_animation',frameWidth=fw,frameHeight=fh,frames=im.width//fw)
  elif 'EyeinJar' in archive:row.update(kind='prop_animation',frameWidth=128,frameHeight=128,frames=im.width//128)
  else:row['kind']='ui_atlas_or_prop'
 index.append(row)
(r/'packs/catalog.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(r/'packs/ScreenPet-Packs-Completo.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p,name,_ in files:z.write(p,'source-packs/'+name)
 for p in sorted((r/'assets-hd').rglob('*.png')):z.write(p,'assets-hd/'+str(p.relative_to(r/'assets-hd')))
 z.write(r/'packs/catalog.json','catalog.json');z.write(r/'packs/ORIGEM-E-LICENCAS.md','ORIGEM-E-LICENCAS.md')
print(f'Bundled {len(files)} source assets and {len(list((r/"assets-hd").rglob("*.png")))} HD sprite sheets')
