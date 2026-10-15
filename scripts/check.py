#!/usr/bin/env python3
"""Check generated HTML links, metadata, and feeds without a browser."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
errors=[]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[];self.ids=[];self.h1=0;self.title=False;self.viewport=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.title=True
        if tag=='meta' and a.get('name')=='viewport':self.viewport=True
        if tag=='img' and not a.get('alt'):errors.append('Image missing alt text')
        for attr in ['href','src']:
            if attr in a:self.links.append(a[attr])
pages={}
for path in [ROOT/'index.html',*(ROOT/'blog').rglob('*.html'),*(ROOT/'publications').glob('*.html'),*(ROOT/'cv').glob('*.html')]:
    p=Page();p.feed(path.read_text());pages[path.resolve()]=p
    if p.h1!=1 or not p.title or not p.viewport:errors.append(f'{path}: missing heading/title/viewport')
    if len(p.ids)!=len(set(p.ids)):errors.append(f'{path}: duplicate IDs')
for path,p in pages.items():
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{path.name}: missing target {link}')
        if u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'Broken anchor: {link}')
for path in [ROOT/'sitemap.xml',ROOT/'blog/feed.xml']:ET.parse(path)
assert not errors,'\n'.join(errors)
print(f'Passed: {len(pages)} pages; internal links, anchors, image alt text, metadata, sitemap, and Atom feed.')
