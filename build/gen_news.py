#!/usr/bin/env python3
"""Сторінка «Новини» (news.html) з content/news.json. Блок на головній — у build.py (news())."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_solutions import chrome, e, ROOT
from build import news, MONTHS

N = json.load(open(os.path.join(ROOT, 'content/news.json')))
CSS = '''<style>
.news4{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.nc{display:flex;flex-direction:column;background:var(--bg2);border-radius:8px;overflow:hidden;color:var(--ink)}
.nc img{width:100%;aspect-ratio:16/10;object-fit:cover}
.nc div{padding:16px 18px 20px}
.nc small{display:flex;align-items:center;gap:10px;font-size:14px;color:var(--muted)}
.nc .tag{font-size:13px;color:var(--blue);background:#fff;border:1px solid var(--line);border-radius:4px;padding:3px 9px}
.nc h3{font-size:18px;line-height:1.35;font-weight:500;margin-top:10px}
@media (max-width:1000px){.news4{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.news4{grid-template-columns:1fr}}
</style>'''

if __name__ == '__main__':
    body = f'''{CSS}<main><section class="blk"><div class="wrap"><div class="eyebrow">{e(N['eyebrow'])}</div><h1 class="st" style="margin-bottom:36px">{e(N['title'])}</h1>{news(dict(N, count=999))}</div></section></main>'''
    open(os.path.join(ROOT, 'news.html'), 'w').write(chrome(body, N['title'], 'news'))
    print('news: news.html')
