#!/usr/bin/env python3
"""Генерує solutions.html (список рішень) і sol-<slug>.html з content/solutions.json."""
import json, os, re, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
from uk import UK
C = os.path.join(ROOT, 'content/')
e = lambda s: html.escape(str(s), quote=True)
D = json.load(open(C + 'solutions.json'))
ser = json.load(open(C + 'catalog/sensor_series.json')); cat = json.load(open(C + 'catalog/iot_catalog.json'))
files = json.load(open(C + 'catalog/series_files.json')); specs = json.load(open(C + 'catalog/specs.json'))
img = lambda n: 'img/cat/cat-' + n.split('?')[0].split('/')[-1].rsplit('.', 1)[0] + '.webp'
jslug = lambda m: re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', m.lower()))
DEV = {}
for s in ser:
    if s['key'] in files:
        for p in s['products']: DEV.setdefault(p['model'], (img(p['img']), files[s['key']], UK.get(p['name'], p['name'])))
for src, k in [('lorawan-gateway', 'gateways'), ('lorawan-controller', 'controllers')]:
    for x in cat[src]['products']: DEV.setdefault(x['title'][0], (img(x['img']), files[k], UK.get(' '.join(x['title'][1:]), ' '.join(x['title'][1:]))))
EXTRA = {'UR32': ('img/ur32.webp', 's-routers.html#m-ur32', 'Промисловий 4G-роутер'),
         'UR35': ('img/ur32.webp', 's-routers.html#m-ur35', 'Промисловий 4G-роутер'),
         'UR75': ('img/ur75.webp', 's-routers.html#m-ur75', 'Промисловий 5G-роутер')}
OURS = {'EM300-TH': 'em300-th', 'EM300-MCS': 'em300-mcs', 'EM300-MLD': 'em300-mld', 'EM300-SLD/ZLD': 'em300-sld', 'EM300-DI': 'em300-di'}
def dev(m):
    if m in OURS: i, f, n = 'img/' + OURS[m] + '.webp', 'catalog.html#m-' + OURS[m], DEV.get(m, ('', '', m))[2]; ext = False
    elif m in EXTRA: i, f, n = EXTRA[m]; ext = f.startswith('http')
    else:
        i, f, n = DEV[m]; f = f + ('#m-' + jslug(m) if m in specs else ''); ext = False
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="dev" href="{e(f)}"{t}><div class="di"><img src="{e(i)}" alt="{e(m)}" loading="lazy"></div><b>{e(m)}</b><span>{e(n)}</span></a>'
def case(k):
    c = D['cases'][k]; t = ' target="_blank" rel="noopener"' if c['link'].startswith('http') else ''
    return f'<a class="cc rv" href="{e(c["link"])}"{t}><img src="{e(c["img"])}" alt="" loading="lazy"><span class="chip">{e(c["src"])}</span><h3>{e(c["title"] if "title" in c else c["t"])}</h3></a>'
def chrome(body, title, key):
    t = open(os.path.join(ROOT, 'build/solutions_tpl.html')).read()
    hdr = open(os.path.join(ROOT, 'build/header.html')).read().replace(' aria-current="page"', '').replace('<a href="./#scenarios">Рішення</a>', '<a href="solutions.html" aria-current="page">Рішення</a>')
    css = open(os.path.join(ROOT, 'build/chrome.css')).read()
    return t.replace('</style>', css + '</style>', 1).replace('<!--HEADER-->', hdr).replace('<!--FOOTER-->', open(os.path.join(ROOT, 'build/footer.html')).read()).replace('__TITLE__', e(title)).replace('__BODY__', body)

def page(k, s):
    others = ''.join(f'<a class="oc" href="sol-{o}.html"><img src="{e(D["items"][o]["tile"])}" alt="" loading="lazy"><b>{e(D["items"][o]["title"])}</b></a>' for o in D['order'] if o != k)
    apps_l = ''.join(f'<button type="button"{" class=\"on\"" if i == 0 else ""}>{e(a["t"])}</button>' for i, a in enumerate(s['apps']))
    apps_p = ''.join(f'<div class="ap{" on" if i == 0 else ""}"><div class="where">Де: {e(a["where"])}</div><h3>{e(a["t"])}</h3><p>{e(a["d"])}</p>'
                     + (f'<div class="apimg"><img src="{e(a["img"])}" alt="" loading="lazy"></div>' if a.get('img') else '')
                     + '<div class="devs">' + ''.join(dev(m) for m in a['devices']) + '</div></div>' for i, a in enumerate(s['apps']))
    body = f'''<div class="hero"><img src="{e(s['hero'])}" alt=""><div class="tx wrap"><div class="eyebrow">Рішення</div><h1>{e(s['title'])}</h1><p>{e(s['lead'])}</p><a class="btn" href="./#contact">Обговорити проєкт</a></div></div>
<div class="tabs"><div class="wrap"><nav aria-label="Розділи"><a href="#problems" class="on">Виклики</a><a href="#solution">Рішення</a><a href="#apps">Застосування</a><a href="#benefits">Переваги</a><a href="#cases">Кейси</a></nav>
<div class="bc"><a href="./">Головна</a> › <a href="solutions.html">Рішення</a> › {e(s['title'])}</div></div></div>
<main>
<section id="problems" class="blk"><div class="wrap"><h2 class="st center">З чим стикаються на об'єктах</h2>
<div class="pgrid">{''.join(f'<div class="pc rv"><div class="im"><img src="{e(p["img"])}" alt="" loading="lazy"></div><h3>{e(p["t"])}</h3><p>{e(p["d"])}</p></div>' for p in s['problems'])}</div></div></section>
<section id="solution" class="blk alt"><div class="wrap intro"><div><div class="eyebrow">Як це працює</div><h2 class="st">{e(s['intro']['t'])}</h2><p>{e(s['intro']['d'])}</p></div><div class="pic rv"><img src="{e(s['intro']['img'])}" alt="" loading="lazy"></div></div></section>
<section id="apps" class="blk"><div class="wrap"><h2 class="st center">Застосування й обладнання</h2><div class="apps rv"><div class="al" role="tablist">{apps_l}</div><div>{apps_p}</div></div></div></section>
<section id="benefits" class="blk alt"><div class="wrap"><h2 class="st center">Що ви отримуєте</h2><div class="ben">{''.join(f'<div class="rv"><i>0{i+1}</i><b>{e(b[0])}</b><span>{e(b[1])}</span></div>' for i, b in enumerate(s['benefits']))}</div></div></section>
<section id="cases" class="blk"><div class="wrap"><h2 class="st center">Реалізовані проєкти</h2><div class="cg">{''.join(case(c) for c in s['cases'])}</div></div></section>
<section class="blk alt" style="padding-block:72px"><div class="wrap"><h2 class="st">Інші рішення</h2><div class="others">{others}</div></div></section>
<section class="blk" style="padding-block:64px"><div class="wrap"><div class="cta"><div><h2>Обговоримо ваш об'єкт</h2><p>Підберемо обладнання й покажемо, як це працюватиме у вас.</p></div><a class="btn w" href="./#contact">Залишити заявку</a></div></div></section>
</main>'''
    open(os.path.join(ROOT, f'sol-{k}.html'), 'w').write(chrome(body, s['title'], k))

def hub():
    cards = ''.join(f'<a class="hc rv" href="sol-{k}.html"><img src="{e(D["items"][k]["tile"] if k!="energy" else D["items"][k]["hero"])}" alt="" loading="lazy"><h2>{e(D["items"][k]["title"])}</h2><p>{e(D["items"][k]["short"])}</p><span class="btn">Детальніше</span></a>' for k in D['order'])
    ng = json.load(open(C + 'netguard.json'))
    cards += f'<a class="hng rv" href="zakhyst.html"><img src="img/sol/netguard-ur75.webp" alt="Промисловий роутер Milesight UR75" loading="lazy"><span class="tg ok">✓ ваш сервер</span><span class="tg no">✕ невідома адреса</span><div class="tx"><div class="eyebrow">Новий напрям</div><h2>{e(ng["title"])}</h2><p>{e(ng["short"])}</p><span class="btn">Детальніше</span></div><small class="src">Фото: Milesight UR75</small></a>'
    body = f'''<div class="hero" style="height:400px;min-height:360px"><img src="img/ms/ms-hero-uc722.webp" alt=""><div class="tx wrap"><div class="eyebrow">Рішення</div><h1>Рішення під ваш об'єкт</h1><p>Енергетика, будівлі, промисловість, повітря, вода й агро — бездротовий збір даних і автоматизація.</p></div></div>
<main><section class="blk"><div class="wrap"><div class="hub">{cards}</div></div></section>
<section class="blk" style="padding-block:24px 72px"><div class="wrap"><div class="cta"><div><h2>Не знайшли свій випадок?</h2><p>Розкажіть про задачу — підкажемо, що підійде.</p></div><a class="btn w" href="./#contact">Залишити заявку</a></div></div></section></main>'''
    open(os.path.join(ROOT, 'solutions.html'), 'w').write(chrome(body, 'Рішення', 'hub'))

if __name__ == '__main__':
    for k in D['order']: page(k, D['items'][k])
    hub(); print('solutions:', ', '.join('sol-%s.html' % k for k in D['order']))
