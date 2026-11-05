from pathlib import Path
import base64,json
r=Path(__file__).resolve().parents[1];assets=r/'app/src/main/assets'
catalog=json.loads((assets/'pets.json').read_text())
sources=['data:image/png;base64,'+base64.b64encode((assets/e['file']).read_bytes()).decode() for e in catalog]
def safe_json(value):return json.dumps(value,ensure_ascii=False).replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
text=(r/'preview/template.html').read_text().replace('__SOURCES__',json.dumps(sources)).replace('__CATALOG__',safe_json(catalog)).replace('__DEFAULTS__',safe_json(json.loads((assets/'defaults.json').read_text())))
(r/'preview/gato-de-tela.html').write_text(text)
print('Preview rebuilt:',len(catalog),'characters')
