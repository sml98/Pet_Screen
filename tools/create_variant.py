#!/usr/bin/env python3
"""Create an isolated, branded Android project with a chosen catalog character."""
from pathlib import Path
from PIL import Image
from xml.sax.saxutils import escape
import argparse,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--application-id',required=True);p.add_argument('--app-name',required=True);p.add_argument('--pet-name',required=True);p.add_argument('--character-id',required=True)
 p.add_argument('--personality',choices=['balanced','grumpy','affectionate','cute','lazy'],default='balanced');p.add_argument('--sex',choices=['male','female'],default='male');p.add_argument('--theme',choices=['cozy','pastel','fantasy'],default='cozy')
 args=p.parse_args();out=args.output.resolve()
 if not re.fullmatch(r'[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){2,}',args.application_id):p.error('Use a lowercase application id with at least three components, e.g. br.com.ana.pet')
 if out.exists() or ROOT==out or ROOT in out.parents:p.error('Output must be a new directory outside this base repository')
 if not args.app_name.strip() or not args.pet_name.strip():p.error('Names cannot be empty')
 catalog=json.loads((ROOT/'app/src/main/assets/pets.json').read_text());entry=next((e for e in catalog if e['id']==args.character_id),None)
 if not entry:p.error('Unknown character id. Import its sheet before creating the variant.')
 out.mkdir(parents=True)
 for directory in ['app','gradle','tools','skills','docs']:
  shutil.copytree(ROOT/directory,out/directory,ignore=shutil.ignore_patterns('build','.gradle','__pycache__','*.jks','*.keystore','*.p12','*.pfx','*.key','*.apk','*.aab','credentials.json','secrets.json','.env','local.properties','signing-backup'))
 (out/'preview').mkdir();shutil.copy(ROOT/'preview/template.html',out/'preview/template.html')
 for file in ['build.gradle','settings.gradle','gradlew','gradlew.bat','.gitignore','LICENSE','AGENTS.md']:
  shutil.copy2(ROOT/file,out/file)
 (out/'packs').mkdir();shutil.copy(ROOT/'packs/ORIGEM-E-LICENCAS.md',out/'packs/ORIGEM-E-LICENCAS.md');(out/'.github/workflows').mkdir(parents=True);shutil.copy(ROOT/'.github/workflows/android.yml',out/'.github/workflows/android.yml')
 assets=out/'app/src/main/assets'
 for item in catalog:
  if item['file']!=entry['file']:(assets/item['file']).unlink(missing_ok=True)
 (assets/'pets.json').write_text(json.dumps([entry],ensure_ascii=False,indent=2)+'\n')
 defaults={'name':args.pet_name.strip()[:24],'sex':['male','female'].index(args.sex),'personality':['balanced','grumpy','affectionate','cute','lazy'].index(args.personality),'skin':0,'fur':0,'eyes':0,'outfit':0,'theme':['cozy','pastel','fantasy'].index(args.theme),'size':88}
 (assets/'defaults.json').write_text(json.dumps(defaults,ensure_ascii=False,indent=2)+'\n')
 build=out/'app/build.gradle';build.write_text(re.sub(r"applicationId '[^']+'",f"applicationId '{args.application_id}'",build.read_text()))
 (out/'app/src/main/res/values/strings.xml').write_text('<resources><string name="app_name">'+escape(args.app_name.strip().replace(chr(92),chr(92)*2).replace(chr(39),chr(92)+chr(39)).replace(chr(34),chr(92)+chr(34)).replace('@',chr(92)+'@').replace('?',chr(92)+'?'))+'</string></resources>\n')
 im=Image.open(assets/entry['file']).convert('RGBA');frame=im.crop((0,0,entry['frameWidth'],entry['frameHeight']));icon=Image.new('RGBA',(256,256));scale=min(256/frame.width,256/frame.height);frame=frame.resize((round(frame.width*scale),round(frame.height*scale)),Image.Resampling.NEAREST);icon.paste(frame,((256-frame.width)//2,(256-frame.height)//2),frame);icon.save(out/'app/src/main/res/drawable/cat_icon.png')
 (out/'README.md').write_text(f'# {args.app_name}\n\nPet personalizado baseado no Android Screen Pet Kit.\n\n- Pacote: `{args.application_id}`\n- Personagem: {entry["name"]}\n- Nome inicial: {defaults["name"]}\n- Personalidade: {args.personality}\n\nConfigure Android SDK 35/JDK 17 e execute `./gradlew assembleDebug`. Para release, configure sua própria chave por variáveis RELEASE_STORE_FILE, RELEASE_STORE_PASSWORD, RELEASE_KEY_ALIAS e RELEASE_KEY_PASSWORD. O workflow GitHub gera debug sem secrets.\n\nA licença MIT refere-se ao código. Verifique os direitos do pack escolhido antes de publicar. Nenhuma chave de assinatura foi copiada para este projeto.\n')
 subprocess.run([sys.executable,str(out/'tools/rebuild_preview.py')],check=True)
 print(json.dumps({'output':str(out),'applicationId':args.application_id,'character':entry['id'],'profile':defaults},ensure_ascii=False))
if __name__=='__main__':main()
