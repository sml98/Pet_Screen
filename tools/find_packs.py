#!/usr/bin/env python3
"""Discover candidate sprite packs on OpenGameArt and Kenney; never infer a license."""
import argparse,json,re,time
from urllib.request import Request,urlopen
from urllib.parse import urlencode,urljoin,urlparse
from html.parser import HTMLParser
from pathlib import Path
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.href=None;self.label=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.href=dict(attrs).get('href');self.label=[]
 def handle_data(self,data):
  if self.href:self.label.append(data)
 def handle_endtag(self,tag):
  if tag=='a' and self.href:self.links.append((self.href,' '.join(self.label).strip()));self.href=None

def discover(query):
 searches=[('OpenGameArt','https://opengameart.org/art-search-advanced?'+urlencode({'keys':query,'sort_by':'count','sort_order':'DESC'}),'/content/'),('Kenney','https://kenney.nl/assets?'+urlencode({'search':query}),'/assets/')]
 tokens=[t for t in re.findall(r'[a-z0-9]+',query.lower()) if len(t)>2 and t not in {'sprite','sprites','asset','assets','pack','packs','pixel','art','animated','animation'}]
 result={'query':query,'candidates':[],'searches':[],'note':'Candidates are search results, not verified recommendations. Inspect art, frame geometry, original author and license before downloading or redistributing.'};seen=set()
 for source,url,prefix in searches:
  record={'source':source,'url':url,'status':'ok'}
  try:
   with urlopen(Request(url,headers={'User-Agent':'ScreenPetKit/1.0 (asset research)'}),timeout=20) as response:html=response.read(2000000).decode('utf-8',errors='replace')
   parser=Links();parser.feed(html)
   for href,title in parser.links:
    link=urljoin(url,href);parsed=urlparse(link)
    relevant=not tokens or any(token in (title+' '+parsed.path).lower() for token in tokens)
    if relevant and parsed.netloc==urlparse(url).netloc and parsed.path.startswith(prefix) and len(parsed.path)>len(prefix) and link not in seen and title:
     seen.add(link);result['candidates'].append({'source':source,'title':re.sub(r'\s+',' ',title)[:180],'url':link,'licenseStatus':'not verified'})
  except Exception as exc:record['status']='unavailable';record['error']=str(exc)
  result['searches'].append(record)
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--query',required=True);parser.add_argument('--output',type=Path);args=parser.parse_args();data=discover(args.query);text=json.dumps(data,ensure_ascii=False,indent=2)
 if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text+'\n')
 print(text)
