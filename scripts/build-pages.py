#!/usr/bin/env python3
"""Export a DoF static public directory for a GitHub Pages project path.
No network, publishing, credentials, framework build, or image conversion.
"""
from __future__ import annotations
import argparse, hashlib, html, json, pathlib, posixpath, re, shutil, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin, unquote
SITE='https://dof-embodied-ai.steven12123.chatgpt.site'
TEXT={'.html','.css','.js','.json','.txt','.srt','.svg'}
ALLOWED=TEXT|{'.png','.jpg','.jpeg','.webp','.pdf'}
IMAGES={'.png','.jpg','.jpeg','.webp','.svg'}
def read(p):
 with p.open('rb') as f:return f.read(p.stat().st_size)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--source',required=True,type=pathlib.Path);a.add_argument('--output',required=True,type=pathlib.Path);a.add_argument('--repo-base',required=True);a.add_argument('--site-origin',default='https://dld0621.github.io');a.add_argument('--source-commit',default='');args=a.parse_args()
 source=args.source.resolve();out=args.output.resolve();base='/'+args.repo_base.strip('/')+'/' if args.repo_base.strip('/') else '/';origin=args.site_origin.rstrip('/');siteurl=origin+base
 if not source.is_dir() or source==out or source in out.parents or out in source.parents:raise SystemExit('Source and output must be separate directories.')
 if not re.fullmatch(r'/(?:[A-Za-z0-9_.-]+/)*',base):raise SystemExit('repo-base must be a plain URL directory path.')
 if urlsplit(origin).scheme!='https':raise SystemExit('site-origin must be HTTPS.')
 marker=out/'.dof-pages-export.json';previous={}
 if marker.is_file():previous=json.loads(read(marker))
 elif out.exists() and any(out.iterdir()):raise SystemExit('Refusing a nonempty output without the export manifest.')
 def url(value):
  if value.startswith(SITE+'/media/'):return value
  if value==SITE or value.startswith(SITE+'/'):return siteurl+value[len(SITE):].lstrip('/')
  if value.startswith('/media/'):return SITE+value
  if value.startswith('/') and not value.startswith('//'):
   if base!='/' and (value==base.rstrip('/') or value.startswith(base)):return value
   return base+value.lstrip('/')
  return value
 def walk(x):
  if isinstance(x,dict):return {k:walk(v) for k,v in x.items()}
  if isinstance(x,list):return [walk(v) for v in x]
  return url(x) if isinstance(x,str) else x
 release_edits={}
 def transform(text,rel):
  if rel.endswith('.html') and '本地成片，未上传、未发布。' in text:
   release_edits[rel]=text.count('本地成片，未上传、未发布。');text=text.replace('本地成片，未上传、未发布。','DoF 公开课程。')
  if rel=='catalog.js':
   assert text.startswith('window.DOF_CATALOG = ')
   obj=json.loads(text.split('=',1)[1].strip().rstrip(';'));return 'window.DOF_CATALOG = '+json.dumps(walk(obj),ensure_ascii=False,separators=(',',':'))+';\n'
  if rel.endswith('.json'):
   return json.dumps(walk(json.loads(text.lstrip('\ufeff'))),ensure_ascii=False,separators=(',',':'))+'\n'
  if rel.endswith(('.html','.js','.css','.svg')):
   # Quoted root URLs include HTML attrs and embedded JavaScript strings.
   text=re.sub(r'''(["'])(/(?!/)[^"'\s<>]*)\1''',lambda m:m[1]+url(m[2])+m[1],text)
   text=re.sub(r'''((?:href|src|poster|action|content)\s*=\s*)(["'])(.*?)\2''',lambda m:m[1]+m[2]+url(m[3])+m[2],text,flags=re.I)
   text=re.sub(r'''url\(\s*(/[^\s)]+)\s*\)''',lambda m:'url('+url(m[1])+')',text)
  return text
 payload={};original={};excluded=[]
 for p in sorted(source.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(source).as_posix()
  if any(x.startswith('.') for x in p.relative_to(source).parts) or p.suffix.lower() not in ALLOWED:excluded.append(rel);continue
  if p.is_symlink():raise SystemExit('Refusing symlink '+rel)
  raw=read(p);original[rel]=raw
  if p.suffix in TEXT:
   text=raw.decode('utf-8');payload[rel]=transform(text,rel).encode('utf-8')
  else:payload[rel]=raw
 # All image bytes stay exactly as shipped, including original research figures.
 images=[r for r in payload if pathlib.Path(r).suffix in IMAGES]
 assert all(payload[r]==original[r] for r in images),'Image bytes changed'
 bad=[]
 privacy=re.compile(r'(?:/(?:Users|private|home)/|file:\/\/|localhost(?=[:/])|127\.0\.0\.1|[A-Z]:\\Users\\)')
 secret=re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|Bearer [A-Za-z0-9._-]{24,})')
 for rel,raw in payload.items():
  if pathlib.Path(rel).suffix not in TEXT:continue
  text=raw.decode('utf-8')
  for match in privacy.finditer(text):bad.append({'file':rel,'kind':'private path','offset':match.start()})
  for match in secret.finditer(text):bad.append({'file':rel,'kind':'credential pattern','offset':match.start()})
 if bad:raise SystemExit('Public-content audit failed: '+json.dumps(bad))
 catalog=json.loads(payload['catalog.js'].decode().split('=',1)[1].strip().rstrip(';'));course=json.loads(payload['retargeting/course-data.json'])
 variants=[v for item in catalog['items'] for v in item['variants']]
 assert len(catalog['items'])>=41 and len(variants)>=52
 assert len(course['chapters'])==6 and len(course['methods'])==28
 assert all(v['src'].startswith(SITE+'/media/') for v in variants)
 courses={k:json.loads(v)for k,v in payload.items()if k.endswith('/course-data.json')}
 assert all(not c.get('preview',False)for c in courses.values())
 assert all(v['src'].startswith(SITE+'/media/')for c in courses.values()for v in c['chapters'])
 references=[]
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for k,v in attrs:
    if k in ('src','href','poster') and v:references.append((current,v))
 def jsonlinks(x,current):
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ('src','poster','featureImage','url') and isinstance(v,str):references.append((current,v))
    else:jsonlinks(v,current)
  elif isinstance(x,list):
   for v in x:jsonlinks(v,current)
 for current,raw in payload.items():
  if current.endswith('.html'):
   parser=Links();parser.feed(raw.decode())
  elif current.endswith('.css'):
   for m in re.finditer(r'''url\(["']?([^)'"\s]+)''',raw.decode()):references.append((current,m[1]))
 jsonlinks(catalog,'index.html')
 for name,c in courses.items():jsonlinks(c,name.replace('course-data.json','index.html'))
 missing=[];checked=set()
 for current,ref in references:
  if ref.startswith(('data:','#','mailto:','tel:','javascript:')):continue
  full=urljoin(siteurl+current,html.unescape(ref));parsed=urlsplit(full)
  if parsed.netloc!=urlsplit(origin).netloc:continue
  if not parsed.path.startswith(base):missing.append({'from':current,'url':ref,'reason':'escaped project base'});continue
  relative=unquote(parsed.path[len(base):]);relative=posixpath.normpath(relative)
  if relative in ('','.'):relative='index.html'
  if parsed.path.endswith('/'):relative=relative.rstrip('/')+'/index.html' if relative!='index.html' else relative
  if relative not in payload:missing.append({'from':current,'url':ref,'resolved':relative})
  checked.add(relative)
 if missing:raise SystemExit('Missing internal resources: '+json.dumps(missing,ensure_ascii=False))
 # No unwanted root URLs remain in data or HTML/JS/CSS.
 roots=[]
 for rel,raw in payload.items():
  if pathlib.Path(rel).suffix not in TEXT:continue
  text=raw.decode()
  for m in re.finditer(r'''(["'])(/(?!/)[^"'\s<>]*)\1''',text):
   if base!='/' and not (m[2].startswith(base) or m[2]==base.rstrip('/')):roots.append({'file':rel,'url':m[2]})
 if roots:raise SystemExit('Unbound root URLs: '+json.dumps(roots))
 payload['.nojekyll']=b''
 payload['README.md']=f'''# DoF · Embodied AI

A bilingual educational library for embodied AI, robotics papers and practical research concepts.

- **Website:** [{siteurl}]({siteurl})
- **Dexterous retargeting course:** [{siteurl}retargeting/]({siteurl}retargeting/)
- **Research map:** [DoF Embodied AI Paper Analysis](https://github.com/Dld0621/Embodied-AI-Paper-Analysis)

The static site contains {len(catalog['items'])} library entries and references to {len(variants)} videos. Courses include dexterous retargeting, VLA and world models, with bilingual method profiles and interactive teaching experiments. Chinese and English can be switched in the interface. Original figures and author demonstrations retain their source citations; the teaching experiments are illustrations, not independent benchmark results.

## Hosting

GitHub Pages serves this repository from the `main` branch, root directory. `.nojekyll` preserves the static files. No Node installation, server, Worker, API key, or build action is needed to serve it.

Video files are intentionally not stored in this repository. Playback keeps using the existing public media endpoint at `{SITE}/media/`. This preserves the full video library without duplicating large video files in Git. That media service must remain available for playback; the Pages site is a static frontend, not a migration of video storage.

## Updating the static export

Use a fresh static `public` source directory, then export to a separate destination:

```sh
python3 scripts/build-pages.py --source ./source-public --output ./pages-output --repo-base {base} --site-origin {origin}
```

Review the export manifest and test the project path before replacing the published repository contents. The exporter changes internal links and media URLs, preserves image bytes, checks local resource targets, and refuses detected local filesystem paths or credential patterns. It does not publish or push anything.

## Attribution

Paper figures, quoted research findings, third-party demonstrations and linked media remain subject to their respective authors' terms. This repository does not grant a new license to third-party material or claim author endorsement. See the source links accompanying each item. Narration is AI-generated; videos identify the music and research sources used.
'''.encode('utf-8')
 payload['scripts/build-pages.py']=read(pathlib.Path(__file__).resolve())
 report={'format':'DoF GitHub Pages static export v1','repo_base':base,'site_url':siteurl,'media_origin':SITE,'source_commit':args.source_commit,'catalog_items':len(catalog['items']),'video_references':len(variants),'course_chapters':sum(len(c['chapters'])for c in courses.values()),'method_profiles':sum(len(c['methods'])for c in courses.values()),'image_files_unchanged':len(images),'internal_targets_checked':len(checked),'excluded':excluded,'release_copy_edits':release_edits,'privacy_scan':'passed','root_url_check':'passed','source_media_not_copied':True,'files':{r:{'bytes':len(v),'sha256':sha(v)}for r,v in payload.items()}}
 payload['.dof-pages-export.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
 allowed_previous=set(previous.get('files',{}))|{'.dof-pages-export.json'}
 for rel in payload:
  dest=out/rel
  if dest.exists() and rel not in allowed_previous:raise SystemExit('Refusing unknown existing file '+rel)
 out.mkdir(parents=True,exist_ok=True)
 for rel,raw in payload.items():
  dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 print(json.dumps({k:v for k,v in report.items() if k!='files'}|{'file_count':len(payload),'bytes':sum(map(len,payload.values()))},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
