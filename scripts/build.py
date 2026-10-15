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

def page(title, content, active='About', location='', description='Xidong Wang — Ph.D. candidate at CUHK-Shenzhen. Democratizing progress toward AGI through stronger model architectures, training algorithms, and accessible medical AI.'):
    depth = len(Path(location).parts) if location else 0
    rel = '../' * depth
    nav = ''.join(f'<a href="{rel}{dest}"'+(' aria-current="page"' if label == active else '')+f'>{label}</a>' for label, dest in [('About','index.html'),('Publications','publications/'),('Blog','blog/'),('CV','assets/Xidong_Wang_CV.pdf')])
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Xidong Wang</title><meta name="description" content="{e(description, quote=True)}">
<link rel="canonical" href="{SITE}/{location + '/' if location else ''}"><meta property="og:title" content="{e(title, quote=True)} | Xidong Wang"><meta property="og:description" content="{e(description, quote=True)}"><meta property="og:type" content="{'article' if location.startswith('blog/') else 'website'}"><meta property="og:image" content="{SITE}/assets/portrait.png"><meta property="og:url" content="{SITE}/{location + '/' if location else ''}"><link rel="stylesheet" href="{rel}assets/style.css"><script src="{rel}assets/site.js" defer></script><link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/atom+xml" title="Xidong Wang — Blog" href="{rel}blog/feed.xml"></head>
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
    links = ''.join(f'<a href="{e(p[key], quote=True)}">{label} ↗</a>' for key, label in [('paper','Paper'),('code','Code'),('website','Website'),('impact_source','Industry adoption')] if p.get(key))
    highlight = f'<p class="paper-highlight">{e(p["highlight"])}</p>' if p.get('highlight') else ''
    return f'<article class="paper {"leading" if p.get("leading") else ""}" data-category="{e(p.get("category", ""))}"><h3>{title}</h3><p class="authors">{authors}</p><span class="venue">{e(p["venue"])}</span><span class="paper-links">{links}</span>{highlight}</article>'

def post_card(p, prefix=''):
    highlight = f'<p class="paper-highlight">{e(p["highlight"])}</p>' if p.get('highlight') else ''
    return f'<article class="post-card"><div class="meta"><time datetime="{p["date"]}">{date.fromisoformat(p["date"]).strftime("%B %d, %Y")}</time> · {e(p["tag"])}</div><h2><a href="{prefix}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a href="{prefix}{p["slug"]}/">Read the note →</a></article>'

experience = '''<div class="entry"><div><h3><a href="https://iquestlab.com/">IQuest Research</a></h3><p>Research Intern · Foundation Model Mid-training and Post-training</p><p class="experience-detail">Contributing to STEM reasoning and agent capabilities in foundation model post-training, including <a href="https://iquestlab.github.io/">IQuest-Q1</a>.</p><p class="entry-links"><a href="https://iquestlab.github.io/">IQuest-Q1 blog ↗</a> · <a href="https://github.com/IQuestLab/IQuest-Q1">Model &amp; code ↗</a></p><p class="muted">Beijing, China</p></div><time>Mar. 2026 – Present</time></div>
<div class="entry"><div><h3>Ant Healthcare, Ant Group</h3><p>Research Intern · Rubric Reinforcement Learning</p><p class="experience-detail">Worked on rubric-based reinforcement learning and contributed to the foundation model powering <a href="https://chat.antafu.com/">Ant Afu (蚂蚁阿福)</a>, a widely used AI healthcare app in China with <a href="https://www.yicai.com/brief/103359494.html">150 million users as of September 2026</a>.</p><p class="entry-links"><a href="https://chat.antafu.com/">Ant Afu app &amp; website ↗</a></p><p class="muted">Hangzhou, China</p></div><time>May 2025 – Feb. 2026</time></div>
<div class="entry"><div><h3>Shenzhen Research Institute of Big Data</h3><p>Research Intern · Medical Language Models</p><p class="experience-detail">Contributed to the early development of the <a href="https://github.com/FreedomIntelligence/HuatuoGPT">HuatuoGPT series</a>.</p><p class="entry-links"><a href="https://github.com/FreedomIntelligence/HuatuoGPT">HuatuoGPT project ↗</a></p><p class="muted">Shenzhen, China</p></div><time>Aug. 2022 – Aug. 2023</time></div>'''
education = '''<div class="entry"><div><h3>The Chinese University of Hong Kong, Shenzhen</h3><p>Ph.D. Candidate in Computer Science</p><p class="muted">Advisor: <a href="https://wabyking.github.io/old.html">Prof. Benyou Wang</a></p></div><time>2023 – Present</time></div><div class="entry"><div><h3>Beijing Institute of Technology</h3><p>B.Eng. in Computer Science and Technology</p><p class="muted"><a href="https://xuteli.bit.edu.cn/">Xuteli School</a> · Elite talent development</p></div><time>2019 – 2023</time></div>'''
service = '''<p><strong>Reviewing.</strong> ICLR, ICML, NeurIPS, COLM, TMLR, and ACL Rolling Review.</p><p><strong>Open source.</strong> Lead maintainer of <a href="https://github.com/FreedomIntelligence/Awesome-AI4Med">Awesome-AI4Med</a>, a collection of resources for medical AI. <strong class="paper-highlight">2.9K+ GitHub stars.</strong></p>'''
teaching = '''<div class="entry"><div><h3>CSC6052 · Natural Language Processing</h3><p>Teaching Assistant · CUHK-Shenzhen</p></div><time>Spring 2024 &amp; 2025</time></div><div class="entry"><div><h3>CSC6203 · Large Language Models</h3><p>Teaching Assistant · CUHK-Shenzhen</p></div><time>Fall 2023</time></div><p class="muted">Both courses taught by Prof. Benyou Wang.</p>'''
selected = sorted([p for p in papers if p.get("selected") or p["title"].startswith("Huatuo-26M")], key=lambda p:p["display_order"])
home = f'''<section class="profile" aria-label="Profile"><div><h1>Xidong WANG</h1><p class="role">Ph.D. Candidate · CUHK-Shenzhen</p><p>I am a Ph.D. candidate in Computer Science at <a href="https://www.cuhk.edu.cn/en">The Chinese University of Hong Kong, Shenzhen</a>, advised by <a href="https://wabyking.github.io/old.html">Prof. Benyou Wang</a>. I received my B.Eng. from Beijing Institute of Technology as part of <a href="https://xuteli.bit.edu.cn/">Xuteli School</a>’s elite talent program.</p><p>My goal is to democratize progress toward AGI. I develop architectural and algorithmic methods that advance model capabilities while remaining efficient enough for researchers with modest resources to explore, contribute to, and build upon. (<a href="https://arxiv.org/abs/2409.02889">LongLLaVA</a>; T-Tuning and PPO+, forthcoming.)</p><p>My earlier work in medical AI was motivated by the same goal: using AI for social good and making its benefits more widely accessible through open-source datasets, benchmarks, and multilingual medical models. (<a href="https://arxiv.org/abs/2602.09653">ClinAlign</a>, <a href="https://aclanthology.org/2024.naacl-long.343/">CMB</a>, <a href="https://arxiv.org/abs/2403.03640">Apollo</a>, <a href="https://arxiv.org/abs/2410.10626">ApolloMoE</a>, <a href="https://github.com/FreedomIntelligence/HuatuoGPT">Huatuo series</a>, <a href="https://aclanthology.org/2025.findings-naacl.211/">Huatuo-26M</a>.)</p><p>I am currently a research intern at <strong><a href="https://iquestlab.com/">IQuest Research</a></strong>.</p><p class="contact">Email: <a href="mailto:xidongwang1@link.cuhk.edu.cn">xidongwang1@link.cuhk.edu.cn</a></p><div class="social"><a href="{SCHOLAR.replace('&','&amp;')}">Google Scholar (2.0K+ citations)</a><span>/</span><a href="https://github.com/wangxidong06">GitHub</a><span>/</span><a href="assets/Xidong_Wang_CV.pdf">CV (PDF)</a></div></div><img class="portrait" src="assets/portrait.png" width="180" height="180" alt="Portrait of Xidong Wang"></section>
<section><h2>Education</h2>{education}</section>
<section><h2>Industry Experience</h2>{experience}</section>
<section aria-labelledby="news-heading"><div class="section-heading news-heading"><h2 id="news-heading">News</h2><span class="scroll-hint" id="news-scroll-hint">Scroll for more ↓</span></div><div class="news-scroll" tabindex="0" role="region" aria-labelledby="news-heading" aria-describedby="news-scroll-hint"><ul class="news">
<li><time>Sep. 2026</time><span><a href="https://iquestlab.github.io/"><strong>IQuest-Q1</strong></a> is out! Contributed to STEM and agent post-training. <a href="https://iquestlab.github.io/">Blog ↗</a></span></li>
<li><time>Sep. 2026</time><span>Two papers accepted to <strong>NeurIPS 2026</strong>, including <strong class="news-highlight">one Oral</strong>! Congratulations to all co-authors!</span></li>
<li><time>Aug. 2026</time><span>Two papers accepted to the <strong>EMNLP 2026 main conference</strong>! Congratulations to all co-authors!</span></li>
<li><time>Apr. 2026</time><span>Two papers accepted to <strong>ACL 2026</strong>! Congratulations to all co-authors!</span></li>
<li><time>Mar. 2026</time><span>Joined <strong><a href="https://iquestlab.com/">IQuest Research</a></strong> to work on foundation model post-training for STEM reasoning and agents.</span></li>
<li><time>Jan. 2026</time><span>One paper accepted to <strong>ICLR 2026</strong>: <a href="https://arxiv.org/abs/2602.16747">LiveClin</a>! Congratulations to all co-authors!</span></li>
<li><time>Dec. 2025</time><span>AQ became <a href="https://chat.antafu.com/"><strong>Ant Afu (蚂蚁阿福)</strong></a>! I contributed to the foundation model behind this AI healthcare app. <a href="https://chat.antafu.com/">Try it ↗</a></span></li>
<li><time>2025</time><span><strong>ApolloMoE</strong> accepted to ICLR 2025, and <strong>LongLLaVA</strong> to Findings of EMNLP 2025!</span></li>
</ul></div></section>
<section><div class="section-heading"><h2>Selected publications</h2><a href="publications/">All publications →</a></div><p class="meta">Selected first- and co-first-author papers. * Equal contribution.</p>{''.join(paper_html(p) for p in selected)}</section>
<section><h2>Teaching &amp; service</h2>{teaching}{service}</section>'''
page('About', home)
ordered = sorted(papers, key=lambda p:p['display_order'])
featured = sorted([p for p in papers if p.get('priority',100)<100], key=lambda p:p['priority'])
publication_groups = '<section class="pub-year"><h2>Featured publications</h2>'+''.join(paper_html(p) for p in featured)+'</section>'
publication_groups += '<section class="pub-year"><h2>Other publications</h2>'+''.join(paper_html(p) for p in ordered if p.get('priority',100)==100)+'</section>'
filters = '<div class="filters" aria-label="Filter publications" hidden>' + ''.join(f'<button type="button" data-filter="{label}" aria-pressed="{str(label=="All").lower()}">{label}</button>' for label in ['All','Medical AI','Multimodal','Agents']) + '</div><p class="filter-status" aria-live="polite"></p>'
page('Publications', '<p class="eyebrow">Research</p><h1>Publications</h1><p class="page-intro">Papers on large language models, medical AI, and multimodal learning. See <a href="'+SCHOLAR.replace('&','&amp;')+'">Google Scholar</a> for the latest list.<br>* Equal contribution. First- and co-first-author work is highlighted.</p>'+filters+publication_groups, 'Publications', 'publications')
# Remove previously generated posts so unpublishing a Markdown file removes its public page.
blog = ROOT / 'blog'
if blog.exists():
    for child in blog.iterdir():
        if child.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}-',child.name):
            shutil.rmtree(child)
page('Blog', '<p class="eyebrow">Notes &amp; updates</p><h1>Blog</h1>'+(''.join(post_card(p) for p in posts) or ''), 'Blog', 'blog')
for p in posts:
    page(p['title'],f'<article class="article"><a class="back" href="../">← All posts</a><p class="eyebrow">{e(p["tag"])}</p><h1>{e(p["title"])}</h1><p class="post-meta">Xidong Wang · <time datetime="{p["date"]}">{p["date"]}</time></p>{p["body"]}</article>', 'Blog', 'blog/'+p['slug'], p['summary'])
# Retire the old HTML CV; the navigation now opens the compiled PDF.
if (ROOT/'cv').exists():
    shutil.rmtree(ROOT/'cv')
updated = posts[0]['date'] if posts else date.today().isoformat()
entries = ''.join(f'<entry><title>{e(p["title"])}</title><id>{SITE}/blog/{p["slug"]}/</id><link href="{SITE}/blog/{p["slug"]}/"/><updated>{p["date"]}T00:00:00Z</updated><summary>{e(p["summary"])}</summary></entry>' for p in posts)
(blog/'feed.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Xidong Wang — Blog</title><id>{SITE}/blog/</id><link href="{SITE}/blog/feed.xml" rel="self"/><link href="{SITE}/blog/"/><updated>{updated}T00:00:00Z</updated><author><name>Xidong Wang</name></author>{entries}</feed>')
urls = ['','publications/','blog/']+['blog/'+p['slug']+'/' for p in posts]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}/{u}</loc></url>' for u in urls)+'</urlset>')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print(f'Built {len(urls)} pages and {len(posts)} published blog post(s).')
