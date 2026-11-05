#!/usr/bin/env python3
"""Normalize a regular sprite grid into one horizontal strip and register it."""
from pathlib import Path
from PIL import Image
import argparse,json,re,os
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--sheet',required=True,type=Path);p.add_argument('--id',required=True);p.add_argument('--name',required=True)
 p.add_argument('--frame-width',required=True,type=int);p.add_argument('--frame-height',required=True,type=int)
 p.add_argument('--fps',default=8,type=float);p.add_argument('--count',type=int);p.add_argument('--replace',action='store_true')
 for flag in ['recolor','eyes','accessories']:p.add_argument('--'+flag,action='store_true')
 args=p.parse_args()
 if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',args.id):p.error('--id must contain lowercase letters, digits, underscores or hyphens')
 if not args.name.strip() or min(args.frame_width,args.frame_height)<=0 or not 0<args.fps<=60:p.error('Invalid name, dimensions or fps')
 if (args.eyes or args.accessories) and (args.frame_width,args.frame_height)!=(32,32):p.error('Built-in eye/accessory coordinates require compatible 32x32 characters')
 image=Image.open(args.sheet).convert('RGBA');fw,fh=args.frame_width,args.frame_height
 if image.width%fw or image.height%fh:p.error('Sheet dimensions must be exact multiples of frame dimensions. Crop margins first.')
 columns,rows=image.width//fw,image.height//fh;count=args.count if args.count is not None else columns*rows
 if not 1<=count<=columns*rows or fw*count>16384:p.error('Invalid frame count or strip exceeds 16384px; split the animation into shorter strips')
 catalog_path=ROOT/'app/src/main/assets/pets.json';catalog=json.loads(catalog_path.read_text());existing=next((i for i,e in enumerate(catalog) if e['id']==args.id),None)
 if existing is not None and not args.replace:p.error('Character already exists. Use another id or --replace explicitly.')
 output=Image.new('RGBA',(fw*count,fh))
 for i in range(count):
  x,y=(i%columns)*fw,(i//columns)*fh;output.paste(image.crop((x,y,x+fw,y+fh)),(i*fw,0))
 file='character-'+args.id+'.png';dest=catalog_path.parent/file;temp=dest.with_suffix('.tmp.png');output.save(temp);os.replace(temp,dest)
 entry=dict(id=args.id,name=args.name.strip(),file=file,frameWidth=fw,frameHeight=fh,fps=args.fps,recolor=args.recolor,eyes=args.eyes,accessories=args.accessories)
 if existing is None:catalog.append(entry)
 else:catalog[existing]=entry
 temp=catalog_path.with_suffix('.tmp.json');temp.write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n');os.replace(temp,catalog_path)
 print(json.dumps({'character':entry,'frames':count,'sourceGrid':[columns,rows],'alphaBounds':output.getbbox()},ensure_ascii=False))
if __name__=='__main__':main()
