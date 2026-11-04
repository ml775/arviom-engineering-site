#!/usr/bin/env python3
"""Збирає сторінки сайту з шаблонів і даних у content/.
Запуск: python3 build/build.py   (з кореня сайту)"""
import json, html, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = lambda x: html.escape(str(x), quote=True)
def ext(link): return ' target="_blank" rel="noopener"' if link.startswith('http') else ''

def cases(items):
    big = [c for c in items if c['size'] == 'big']; small = [c for c in items if c['size'] != 'big']
    out = ['<div class="big2">']
    for c in big:
        chips = ''.join(f'<span class="chip">{e(x)}</span>' for x in c['chips'])
        out.append(f'''        <a class="bc{' own' if c.get('own') else ''} rv" href="{e(c['link'])}"{ext(c['link'])}>
          <img src="{e(c['image'])}" alt="">
          <div class="chips">{chips}</div>
          <div><h3>{e(c['title'])}</h3><div class="src">{e(c['note'])}</div></div>
        </a>''')
    out.append('      </div>\n      <div class="small4">')
    for c in small:
        chips = ''.join(f'<span class="chip l">{e(x)}</span>' for x in c['chips'])
        out.append(f'''        <a class="sc rv" href="{e(c['link'])}"{ext(c['link'])}>
          <div class="im"><img src="{e(c['image'])}" alt=""></div>
          <div><div class="chips">{chips}</div><h3>{e(c['title'])}</h3><div class="src">{e(c['note'])}</div></div>
        </a>''')
    out.append('      </div>\n      ')
    return '\n'.join(out)

def software(items):
    out = ['<div class="track" id="track" tabindex="0" aria-label="Наші розробки">']
    for d in items:
        cls = ' class="dv"' if d.get('image_is_device') else ''
        more = f' <a href="{e(d["link"])}">Детальніше →</a>' if d.get('link') else ''
        out.append(f'        <article class="card rv"><div class="im"><img{cls} src="{e(d["image"])}" alt=""><span class="chip">{e(d["tag"])}</span></div><div class="tx"><h3>{e(d["title"])}</h3><p>{e(d["text"])}{more}</p></div></article>')
    out.append('      </div>')
    return '\n'.join(out)

def team(items):
    rows = []
    for p in items:
        ph = f'<img src="{e(p["photo"])}" alt="">' if p.get('photo') else e(p['name'][:1])
        rows.append(f'        <div class="person"><div class="ph">{ph}</div><b>{e(p["name"])}</b>{e(p["role"])}</div>')
    return '<div class="team">\n' + '\n'.join(rows) + '\n      </div>'

def logos(d):
    # логотип, якщо є; інакше назва текстом. text=True — знак + назва поруч (дрібний логотип)
    def cell(l):
        img = f'<img src="{e(l["image"])}" alt="{e(l["name"])}">' if l.get('image') else ''
        txt = e(l['name']) if (not l.get('image') or l.get('text')) else ''
        return f'<div class="ls{" tx" if txt else ""}">{img}{(" <span>" + txt + "</span>") if txt else ""}</div>'
    return f'<div class="logos" aria-label="{e(d["label"])}"><span class="lb">{e(d["label"])}</span>{"".join(cell(l) for l in d["items"])}</div>'

MONTHS = ['січ.', 'лют.', 'бер.', 'квіт.', 'трав.', 'черв.', 'лип.', 'серп.', 'вер.', 'жовт.', 'лист.', 'груд.']

def news(n):
    items = sorted(n['items'], key=lambda x: x['date'], reverse=True)[:n.get('count', 4)]
    out = []
    for x in items:
        y, m, d = x['date'].split('-')
        out.append(f'''        <a class="nc rv" href="{e(x['link'])}"{ext(x['link'])}><img src="{e(x['image'])}" alt="" loading="lazy"><div><small><span class="tag">{e(x['tag'])}</span>{int(d)} {MONTHS[int(m) - 1]} {y}</small><h3>{e(x['title'])}</h3></div></a>''')
    return '<div class="news4">\n' + '\n'.join(out) + '\n      </div>'

def build_index():
    d = json.load(open(os.path.join(ROOT, 'content/home.json')))
    n = json.load(open(os.path.join(ROOT, 'content/news.json')))
    t = open(os.path.join(ROOT, 'build/index_tpl.html')).read()
    t = (t.replace('<!--@CASES-->', cases(d['cases']))
          .replace('<!--@CASES_NOTE-->', f'<p class="note">{e(d["cases_note"])}</p>')
          .replace('<!--@NEWS-->', news(n))
          .replace('<!--@SOFTWARE-->', software(d['software']))
          .replace('<!--@TEAM-->', team(d['team']))
          .replace('<!--@LOGOS-->', logos(d['logos'])))
    open(os.path.join(ROOT, 'index.html'), 'w').write(t)

def build_catalog():
    t = open(os.path.join(ROOT, 'catalog_tpl.html')).read()
    open(os.path.join(ROOT, 'catalog.html'), 'w').write(t.replace('__DATA__', open(os.path.join(ROOT, 'data.js')).read(), 1))

if __name__ == '__main__':
    build_index()
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_series.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_products.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_solutions.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_netguard.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_cases.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_news.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_learn.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/gen_agents.py')], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/seo.py')], check=True)  # завжди останнім
    print('ok: index.html, catalog.html, products.html')
