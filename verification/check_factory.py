from pathlib import Path
from PIL import Image,ImageDraw
import tempfile,shutil,subprocess,json,sys
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='screenpet-import-') as directory:
 tmp=Path(directory);(tmp/'tools').mkdir();(tmp/'app/src/main/assets').mkdir(parents=True)
 shutil.copy(root/'tools/add_character.py',tmp/'tools/add_character.py');(tmp/'app/src/main/assets/pets.json').write_text('[]')
 image=Image.new('RGBA',(96,128));draw=ImageDraw.Draw(image);colors=[(255,0,0,255),(0,255,0,255),(0,0,255,255),(255,255,0,255)]
 for i,color in enumerate(colors):
  x=(i%2)*48;y=(i//2)*64;draw.rectangle((x+2,y+2,x+40,y+60),fill=color)
 image.save(tmp/'input.png')
 subprocess.run([sys.executable,str(tmp/'tools/add_character.py'),'--sheet',str(tmp/'input.png'),'--id','test','--name','Retangular','--frame-width','48','--frame-height','64'],check=True,capture_output=True)
 output=Image.open(tmp/'app/src/main/assets/character-test.png');assert output.size==(192,64)
 for i,color in enumerate(colors):assert output.getpixel((i*48+5,5))==color
 metadata=json.loads((tmp/'app/src/main/assets/pets.json').read_text());assert len(metadata)==1 and not metadata[0]['accessories']
 rejected=subprocess.run([sys.executable,str(tmp/'tools/add_character.py'),'--sheet',str(tmp/'input.png'),'--id','test','--name','Retangular','--frame-width','48','--frame-height','64'],capture_output=True);assert rejected.returncode!=0
print('PASS factory importer: rectangular grid, frame order, transparency, metadata, duplicate protection')
