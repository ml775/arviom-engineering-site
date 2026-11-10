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

ACSS = '''<style>
.art{max-width:780px;margin:0 auto}
.art .meta{display:flex;align-items:center;gap:10px;font-size:14px;color:var(--muted);margin-bottom:14px}
.art .meta .tag{font-size:13px;color:var(--blue);background:#fff;border:1px solid var(--line);border-radius:4px;padding:3px 9px}
.art h1{font-size:40px;line-height:1.15;font-weight:600;margin-bottom:28px}
.art h2{font-size:24px;font-weight:600;margin:34px 0 12px}
.art p{font-size:18px;line-height:1.6;margin-bottom:16px}
.art ul{margin:0 0 16px 0;padding-left:22px}
.art li{font-size:18px;line-height:1.55;margin-bottom:8px}
.art figure{margin:26px 0}
.art figure img{width:100%;border-radius:8px;display:block}
.art figcaption{font-size:13px;color:var(--muted);margin-top:8px}
.art .cta{margin-top:34px;display:flex;gap:14px;flex-wrap:wrap}
.art .btn.ghost{background:#fff;color:var(--blue);border:1px solid var(--blue)}
.art .bc{font-size:14px;color:var(--muted);margin-bottom:22px}.art .bc a{color:var(--muted)}
@media (max-width:560px){.art h1{font-size:30px}.art p,.art li{font-size:17px}}
</style>'''

def article(x):
    y, m, d = x['date'].split('-')
    out = []
    for b in x['body']:
        if 'p' in b: out.append(f'<p>{e(b["p"])}</p>')
        elif 'h' in b: out.append(f'<h2>{e(b["h"])}</h2>')
        elif 'ul' in b: out.append('<ul>' + ''.join(f'<li>{e(i)}</li>' for i in b['ul']) + '</ul>')
        elif 'img' in b: out.append(f'<figure><img src="{e(b["img"])}" alt="" loading="lazy">' + (f'<figcaption>{e(b["cap"])}</figcaption>' if b.get('cap') else '') + '</figure>')
    body = f'''{ACSS}<main><section class="blk"><div class="wrap"><article class="art"><div class="bc"><a href="./">Головна</a> › <a href="news.html">Новини</a></div><div class="meta"><span class="tag">{e(x['tag'])}</span>{int(d)} {MONTHS[int(m) - 1]} {y}</div><h1>{e(x['title'])}</h1>{''.join(out)}<div class="cta"><a class="btn" href="./#contact">Обговорити ваш об'єкт</a><a class="btn ghost" href="news.html">Усі новини</a></div></article></div></section></main>'''
    fn = f"news-{x['slug']}.html"
    open(os.path.join(ROOT, fn), 'w').write(chrome(body, x['title'], 'news'))
    return fn

if __name__ == '__main__':
    body = f'''{CSS}<main><section class="blk"><div class="wrap"><div class="eyebrow">{e(N['eyebrow'])}</div><h1 class="st" style="margin-bottom:36px">{e(N['title'])}</h1>{news(dict(N, count=999))}</div></section></main>'''
    open(os.path.join(ROOT, 'news.html'), 'w').write(chrome(body, N['title'], 'news'))
    print('news: news.html')
    for x in N['items']:
        if x.get('body'):
            fn = article(x)
            print('news:', fn)
