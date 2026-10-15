#!/usr/bin/env python3
"""Build a static academic website. Run from any directory with Python 3."""
from pathlib import Path
from html import escape as e
from datetime import date
import json, re, shutil
import markdown

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://wangxidong06.github.io'
SCHOLAR = 'https://scholar.google.com/citations?user=WJeSzQMAAAAJ&hl=en'
papers = json.loads((ROOT / 'publications.json').read_text())
posts = []
for path in (ROOT / 'content/posts').glob('*.md'):
    if path.name.startswith('_'):
        continue
    raw = path.read_text()
    if not raw.startswith('---\n'):
        raise ValueError(f'Missing metadata: {path.name}')
    _, header, body = raw.split('---', 2)
    meta = {}
    for line in header.strip().splitlines():
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip().strip('"')
    if meta.get('status') != 'published':
        continue
    for key in ['title', 'date', 'summary', 'tag']:
        if not meta.get(key):
            raise ValueError(f'Missing {key}: {path.name}')
    date.fromisoformat(meta['date'])
    meta['slug'] = path.stem
    meta['body'] = markdown.markdown(body, extensions=['fenced_code', 'tables'])
    posts.append(meta)
posts.sort(key=lambda p: p['date'], reverse=True)

def page(title, content, active='About', location='', description='Xidong Wang — Ph.D. candidate at CUHK-Shenzhen. Research on large language models, healthcare AI, and multimodal learning.'):
    depth = len(Path(location).parts) if location else 0
    rel = '../' * depth
    nav = ''.join(f'<a href="{rel}{dest}"'+(' aria-current="page"' if label == active else '')+f'>{label}</a>' for label, dest in [('About','index.html'),('Publications','publications/'),('Blog','blog/'),('CV','cv/')])
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Xidong Wang</title><meta name="description" content="{e(description, quote=True)}">
<link rel="canonical" href="{SITE}/{location + '/' if location else ''}"><meta property="og:title" content="{e(title, quote=True)} | Xidong Wang"><meta property="og:description" content="{e(description, quote=True)}"><meta property="og:type" content="{'article' if location.startswith('blog/') else 'website'}"><meta property="og:image" content="{SITE}/assets/portrait.png"><meta property="og:url" content="{SITE}/{location + '/' if location else ''}"><link rel="stylesheet" href="{rel}assets/style.css"><link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/atom+xml" title="Xidong Wang — Blog" href="{rel}blog/feed.xml"></head>
<body><a class="skip" href="#main">Skip to content</a><div class="shell"><header class="topbar"><a class="brand" href="{rel}index.html">Xidong Wang</a><nav aria-label="Main navigation">{nav}</nav></header>
<main id="main">{content}</main><footer><span>© {date.today().year} Xidong Wang</span><span><a href="mailto:xidongwang1@link.cuhk.edu.cn">Email</a> · <a href="https://github.com/wangxidong06">GitHub</a> · <a href="{SCHOLAR.replace('&','&amp;')}">Google Scholar</a></span></footer></div></body></html>'''
    dest = ROOT / location / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)

def paper_html(p):
    title = e(p['title'])
    if p['paper']:
        title = f'<a href="{e(p["paper"], quote=True)}">{title}</a>'
    authors = e(p['authors']).replace('Xidong Wang', '<strong>Xidong Wang</strong>')
    links = ''.join(f'<a href="{e(p[key], quote=True)}">{label} ↗</a>' for key, label in [('paper','Paper'),('code','Code')] if p[key])
    return f'<article class="paper"><h3>{title}</h3><p class="authors">{authors}</p><span class="venue">{e(p["venue"])}</span><span class="paper-links">{links}</span></article>'

def post_card(p, prefix=''):
    return f'<article class="post-card"><div class="meta"><time datetime="{p["date"]}">{date.fromisoformat(p["date"]).strftime("%B %d, %Y")}</time> · {e(p["tag"])}</div><h2><a href="{prefix}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a href="{prefix}{p["slug"]}/">Read the note →</a></article>'

experience = '''<div class="entry"><div><h3>Ubiquant IQuest Research</h3><p>Research Intern · General LLM Mid-training &amp; Post-training</p><p class="muted">Beijing, China</p></div><time>Mar. 2026 – Present</time></div><div class="entry"><div><h3>Ant Healthcare, Ant Group</h3><p>Research Intern · Rubric Reinforcement Learning</p><p class="muted">Hangzhou, China</p></div><time>May 2025 – Feb. 2026</time></div><div class="entry"><div><h3>Shenzhen Research Institute of Big Data</h3><p>Research Intern · Domain Models</p><p class="muted">Shenzhen, China</p></div><time>Aug. 2022 – Aug. 2023</time></div>'''
education = '''<div class="entry"><div><h3>The Chinese University of Hong Kong, Shenzhen</h3><p>Ph.D. Candidate in Computer Science</p><p class="muted">Advisor: <a href="https://wabyking.github.io/old.html">Prof. Benyou Wang</a></p></div><time>2023 – Present</time></div><div class="entry"><div><h3>Beijing Institute of Technology</h3><p>B.Eng. in Computer Science and Technology</p></div><time>2019 – 2023</time></div>'''
service = '''<p><strong>Reviewing.</strong> ICLR, ICML, NeurIPS, COLM, TMLR, and ACL Rolling Review.</p><p><strong>Open source.</strong> Lead maintainer of <a href="https://github.com/FreedomIntelligence/Awesome-AI4Med">Awesome-AI4Med</a>, a collection of resources for medical AI.</p>'''
teaching = '''<div class="entry"><div><h3>CSC6052 · Natural Language Processing</h3><p>Teaching Assistant · CUHK-Shenzhen</p></div><time>Spring 2024 &amp; 2025</time></div><div class="entry"><div><h3>CSC6203 · Large Language Models</h3><p>Teaching Assistant · CUHK-Shenzhen</p></div><time>Fall 2023</time></div><p class="muted">Both courses taught by Prof. Benyou Wang.</p>'''
selected = [papers[i] for i in [1,2,3,5,4,0]]
home = f'''<section class="profile" aria-label="Profile"><div><h1>Xidong Wang</h1><p class="role">Ph.D. Candidate in Computer Science</p><p class="muted">The Chinese University of Hong Kong, Shenzhen</p><div class="social"><a href="mailto:xidongwang1@link.cuhk.edu.cn">Email ↗</a><a href="{SCHOLAR.replace('&','&amp;')}">Google Scholar ↗</a><a href="https://github.com/wangxidong06">GitHub ↗</a><a href="cv/">CV ↗</a></div></div><img class="portrait" src="assets/portrait.png" width="160" height="160" alt="Xidong Wang's GitHub profile image"></section>
<section class="intro" aria-label="Biography"><p>I am a Ph.D. candidate at <a href="https://www.cuhk.edu.cn/en">CUHK-Shenzhen</a>, advised by <a href="https://wabyking.github.io/old.html">Prof. Benyou Wang</a>. Previously, I received my B.Eng. in Computer Science and Technology from Beijing Institute of Technology.</p><p>I work on <strong>large language models</strong>, with interests in mid-training and post-training, healthcare AI, and efficient multimodal learning. I am currently a research intern at <strong>Ubiquant IQuest Research</strong>, and previously interned at Ant Healthcare and the Shenzhen Research Institute of Big Data.</p><p>Feel free to <a href="mailto:xidongwang1@link.cuhk.edu.cn">get in touch</a> to discuss research and potential collaborations.</p></section>
<section><h2>Research</h2><p>My research spans building capable models and evaluating how they perform in practical settings:</p><ul class="research-list"><li><strong>LLM training and alignment.</strong> Mid-training, post-training, and clinician-grounded principles for healthcare alignment.</li><li><strong>Medical AI and evaluation.</strong> Clinical benchmarks and medical knowledge resources, including <a href="https://arxiv.org/abs/2602.16747">LiveClin</a>, <a href="https://github.com/FreedomIntelligence/CMB">CMB</a>, and <a href="https://github.com/FreedomIntelligence/Huatuo-26M">Huatuo-26M</a>.</li><li><strong>Efficient and accessible models.</strong> Multilingual medical LLMs with <a href="https://github.com/FreedomIntelligence/Apollo">Apollo</a> and <a href="https://github.com/FreedomIntelligence/ApolloMoE">ApolloMoE</a>, and long-context multimodal learning with <a href="https://github.com/FreedomIntelligence/LongLLaVA">LongLLaVA</a>.</li></ul></section>
<section><h2>News</h2><ul class="news"><li><time>2026</time><span>LiveClin at ICLR 2026; healthcare alignment work in Findings of ACL 2026.</span></li><li><time>Mar. 2026</time><span>Joined Ubiquant IQuest Research to work on general LLM mid-training and post-training.</span></li><li><time>2025</time><span>ApolloMoE at ICLR 2025 and LongLLaVA in Findings of EMNLP 2025.</span></li></ul></section>
<section><div class="section-heading"><h2>Selected publications</h2><a href="publications/">All publications →</a></div><p class="meta">* Equal contribution.</p>{''.join(paper_html(p) for p in selected)}</section>
<section><div class="section-heading"><h2>From the blog</h2><a href="blog/">All posts →</a></div>{''.join(post_card(p,'blog/') for p in posts[:2]) or '<p>Research notes and project updates are coming soon.</p>'}</section>
<section><h2>Experience</h2>{experience}</section><section><h2>Education</h2>{education}</section><section><h2>Teaching &amp; service</h2>{teaching}{service}</section>'''
page('About', home)
ordered = sorted(papers, key=lambda p: int(p['venue'][-4:]), reverse=True)
page('Publications', '<p class="eyebrow">Research</p><h1>Publications</h1><p class="page-intro">Papers on large language models, medical AI, and multimodal learning. See <a href="'+SCHOLAR.replace('&','&amp;')+'">Google Scholar</a> for the latest list.<br>* Equal contribution.</p>'+''.join(paper_html(p) for p in ordered), 'Publications', 'publications')
# Remove previously generated posts so unpublishing a Markdown file removes its public page.
blog = ROOT / 'blog'
if blog.exists():
    for child in blog.iterdir():
        if child.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}-',child.name):
            shutil.rmtree(child)
page('Blog', '<p class="eyebrow">Notes &amp; updates</p><h1>Blog</h1><p class="page-intro">A space for new work, research notes, and the ideas behind my projects. <a href="feed.xml">Subscribe via RSS/Atom ↗</a></p>'+(''.join(post_card(p) for p in posts) or '<p>New research notes are coming soon.</p>'), 'Blog', 'blog')
for p in posts:
    page(p['title'],f'<article class="article"><a class="back" href="../">← All posts</a><p class="eyebrow">{e(p["tag"])}</p><h1>{e(p["title"])}</h1><p class="post-meta">Xidong Wang · <time datetime="{p["date"]}">{p["date"]}</time></p>{p["body"]}</article>', 'Blog', 'blog/'+p['slug'], p['summary'])
page('Curriculum vitae',f'<div class="cv"><p class="eyebrow">Curriculum vitae</p><h1>Xidong Wang</h1><p><a href="mailto:xidongwang1@link.cuhk.edu.cn">xidongwang1@link.cuhk.edu.cn</a><br>Ph.D. Candidate · CUHK-Shenzhen</p><p class="print-link">Use your browser’s Print menu to save a PDF.</p><h2>Education</h2>{education}<h2>Research &amp; industry experience</h2>{experience}<h2>Publications</h2>{"".join(paper_html(p) for p in ordered)}<h2>Teaching</h2>{teaching}<h2>Service</h2>{service}<h2>Invited talks</h2><p>The Fin AI · December 2024<br>Efficiently Democratizing Medical LLMs for 50 Languages via a Mixture of Language Family Experts</p><h2>Mentoring</h2><p>Guorui Zheng · 2024 · MSE student at CUHK-Shenzhen; subsequently an Algorithm Engineer at ByteDance.</p></div>','CV','cv')
updated = posts[0]['date'] if posts else date.today().isoformat()
entries = ''.join(f'<entry><title>{e(p["title"])}</title><id>{SITE}/blog/{p["slug"]}/</id><link href="{SITE}/blog/{p["slug"]}/"/><updated>{p["date"]}T00:00:00Z</updated><summary>{e(p["summary"])}</summary></entry>' for p in posts)
(blog/'feed.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Xidong Wang — Blog</title><id>{SITE}/blog/</id><link href="{SITE}/blog/feed.xml" rel="self"/><link href="{SITE}/blog/"/><updated>{updated}T00:00:00Z</updated><author><name>Xidong Wang</name></author>{entries}</feed>')
urls = ['','publications/','blog/','cv/']+['blog/'+p['slug']+'/' for p in posts]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}/{u}</loc></url>' for u in urls)+'</urlset>')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print(f'Built {len(urls)} pages and {len(posts)} published blog post(s).')
