#!/usr/bin/env python3
"""Пошук по сайту: збирає search-index.json з усіх сторінок і моделей каталогу
та підключає search.css / search.js у кожну сторінку. Запускається з build.py перед seo.py."""
import glob, html, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
strip = lambda h: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()
slug = lambda m: re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', m.lower()))
dec = json.JSONDecoder()
SKIP = ('_', 'v2-', 'google')
KIND = [('case-', 'Впровадження'), ('news-', 'Новина'), ('sol-', 'Рішення'), ('s-', 'Серія')]

def jsvar(t, name):
    i = t.find('const %s=' % name)
    return dec.raw_decode(t[i + len(name) + 7:])[0] if i >= 0 else None

def meta(t):
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    ti = re.search(r'<title>(.*?)</title>', t, re.S)
    title = strip(h1.group(1)) if h1 else ''
    if not title and ti: title = strip(ti.group(1)).split(' — ')[0].split(' | ')[0]
    d = re.search(r'<meta name="description" content="([^"]*)"', t)
    return title, (html.unescape(d.group(1)) if d else '')

def run():
    idx = []
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        name = os.path.basename(f)
        if name.startswith(SKIP): continue
        t = open(f, encoding='utf-8').read()
        title, desc = meta(t)
        kind = next((k for p, k in KIND if name.startswith(p)), 'Сторінка')
        if name == 'index.html': continue
        if kind == 'Сторінка':
            ti = re.search(r'<title>(.*?)</title>', t, re.S)
            if ti: title = re.split(r' — | \| | · ', strip(ti.group(1)))[0]
        extra = ''
        if name.startswith('s-'):
            S = jsvar(t, 'S') or {}
            title = S.get('title') or title; desc = S.get('sub') or desc
            for m in jsvar(t, 'MODELS') or []:
                url = name + ('#m-' + slug(m['model']) if m.get('specs') else '')
                kw = ' '.join(m.get('measures') or []) + ' ' + (m.get('purpose') or '')
                idx.append({'t': m['model'], 'd': m.get('name_uk', ''), 'u': url, 'k': 'Продукт', 'i': m.get('img', ''), 'x': kw[:300]})
        if name.startswith('case-'):
            chips = re.findall(r'class="chip[^"]*">([^<]+)<', t)
            extra = ' '.join(dict.fromkeys(strip(c) for c in chips))[:300]
        if title: idx.append({'t': title, 'd': desc[:160], 'u': name, 'k': kind, 'x': extra})
    json.dump(idx, open(os.path.join(ROOT, 'search-index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    tag = '<!--search--><link rel="stylesheet" href="search.css"><script defer src="search.js"></script><!--/search-->'
    n = 0
    for f in glob.glob(os.path.join(ROOT, '*.html')):
        if os.path.basename(f).startswith(SKIP): continue
        t = open(f, encoding='utf-8').read()
        t = re.sub(r'\n?<!--search-->.*?<!--/search-->', '', t, flags=re.S)
        if '</head>' not in t: continue
        open(f, 'w', encoding='utf-8').write(t.replace('</head>', tag + '\n</head>', 1)); n += 1
    print('search:', len(idx), 'records;', n, 'pages')

if __name__ == '__main__':
    run()
