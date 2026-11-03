#!/usr/bin/env python3
"""Сторінка «Захист мереж об'єктів» (zakhyst.html) з content/netguard.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_solutions import chrome, e, ROOT

N = json.load(open(os.path.join(ROOT, 'content/netguard.json')))

CSS = '''<style>
.ng-hero{background:var(--tile);border-bottom:1px solid var(--line)}
.ng-hero .wrap{padding-block:88px 80px;display:block;min-height:0}
.ng-hero .eyebrow{color:var(--blue)}
.ng-hero h1{font-weight:300;font-size:clamp(34px,4.6vw,62px);line-height:1.08;max-width:20ch;color:var(--ink);text-wrap:balance}
.ng-hero h1 span{color:var(--blue)}
.ng-hero p{margin-top:22px;max-width:60ch;color:var(--text);font-size:19px}
.ng-hero .btn{margin-top:30px}
.ng-inc{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:48px;align-items:start}
.ng-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:24px}
.ng-facts div{background:var(--bg2);border-radius:8px;padding:22px 20px}
.ng-facts b{display:block;font-weight:300;font-size:clamp(34px,3.6vw,48px);line-height:1;color:var(--ink);font-variant-numeric:tabular-nums}
.ng-facts span{display:block;margin-top:8px;color:var(--muted);font-size:16px}
.ng-inc p{font-size:19px;color:var(--text)}
.ng-src{margin-top:14px;font-size:14px;color:var(--muted)}
.ng-src a{color:var(--blue)}
.ng-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:36px}
.ng-cards div{background:#fff;border:1px solid var(--line);border-radius:8px;padding:26px}
.ng-cards b{display:block;font-weight:500;font-size:20px;color:var(--ink)}
.ng-cards span{display:block;margin-top:10px;color:var(--muted);font-size:16px}
.ng-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:36px}
.ng-steps div{border-top:2px solid var(--blue);padding-top:20px}
.ng-steps i{font-style:normal;color:var(--blue);font-size:15px}
.ng-steps b{display:block;margin-top:6px;font-weight:500;font-size:20px;color:var(--ink)}
.ng-steps span{display:block;margin-top:10px;color:var(--muted);font-size:16px}
.ng-ex{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:40px;align-items:center;background:var(--soft);border-radius:10px;padding:40px 44px}
.ng-ex .eyebrow{margin-bottom:6px}
.ng-ex h2{font-weight:300;font-size:clamp(26px,2.6vw,34px);line-height:1.15;color:var(--ink)}
.ng-ex p{font-size:18px;color:var(--text)}
@media (max-width:900px){.ng-inc,.ng-ex{grid-template-columns:1fr;gap:24px}.ng-cards,.ng-steps{grid-template-columns:1fr}.ng-ex{padding:28px 22px}.ng-hero .wrap{padding-block:56px}}
@media (max-width:520px){.ng-facts{grid-template-columns:1fr}}
</style>'''


def h1():
    # друге речення — синім
    a, _, b = N['h1'].partition('. ')
    return f'{e(a)}. <span>{e(b)}</span>' if b else e(N['h1'])


def build():
    i, x, f = N['incident'], N['example'], N['final']
    links = ' · '.join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>' for t, u in i['links'])
    body = f'''{CSS}
<div class="ng-hero"><div class="wrap"><div class="eyebrow">{e(N['eyebrow'])}</div><h1>{h1()}</h1><p>{e(N['lead'])}</p><a class="btn" href="./#contact">{e(N['cta'])}</a></div></div>
<main>
<section class="blk"><div class="wrap ng-inc">
<div><div class="eyebrow">{e(i['label'])} · {e(i['date'])}</div><h2 class="st">Хакери розморозили холодильники в сотнях супермаркетів</h2>
<div class="ng-facts">{''.join(f'<div><b>{e(n)}</b><span>{e(t)}</span></div>' for n, t in i['facts'])}</div></div>
<div><p>{e(i['text'])}</p><div class="ng-src">{e(i['src'])}: {links}</div></div>
</div></section>
<section class="blk alt"><div class="wrap"><h2 class="st">{e(N['risks_title'])}</h2>
<div class="ng-cards">{''.join(f'<div class="rv"><b>{e(t)}</b><span>{e(d)}</span></div>' for t, d in N['risks'])}</div></div></section>
<section class="blk"><div class="wrap"><h2 class="st">{e(N['steps_title'])}</h2>
<div class="ng-steps">{''.join(f'<div class="rv"><i>Крок {k + 1}</i><b>{e(t)}</b><span>{e(d)}</span></div>' for k, (t, d) in enumerate(N['steps']))}</div></div></section>
<section class="blk" style="padding-top:0"><div class="wrap"><div class="ng-ex"><div><div class="eyebrow">{e(x['label'])}</div><h2>{e(x['title'])}</h2></div><p>{e(x['text'])}</p></div></div></section>
<section class="blk" style="padding-block:24px 72px"><div class="wrap"><div class="cta"><div><h2>{e(f['title'])}</h2><p>{e(f['text'])}</p></div><a class="btn w" href="./#contact">{e(N['cta'])}</a></div></div></section>
</main>'''
    open(os.path.join(ROOT, 'zakhyst.html'), 'w').write(chrome(body, N['title'], 'netguard'))
    print('netguard: zakhyst.html')


if __name__ == '__main__':
    build()
