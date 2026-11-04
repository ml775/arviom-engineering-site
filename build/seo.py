#!/usr/bin/env python3
"""Пост-обробка всіх *.html: favicon, meta description, Open Graph, canonical, robots.
Запускається останнім кроком build.py. Налаштування — content/site.json (url, noindex)."""
import glob, html, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, 'content/site.json')))
e = lambda x: html.escape(x, quote=True)
strip = lambda h: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()

def describe(t):
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    if m: return html.unescape(m.group(1))
    # перший змістовний абзац після h1 (hero/lead), інакше загальний опис сайту
    i = t.find('<h1'); body = t[i:] if i > 0 else t
    for p in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S):
        s = strip(p)
        if 60 <= len(s): return s[:157].rsplit(' ', 1)[0] + '…' if len(s) > 160 else s
    return S['description']

def og_image(t, f):
    for pat in (r'<meta property="og:image" content="([^"]+)"', r'class="v2-hero"><img src="([^"]+)"', r'<img[^>]+src="(img/(?:cases|sol|hd|learn)/[^"]+\.(?:webp|jpg|png))"'):
        m = re.search(pat, t)
        if m: return m.group(1)
    return S['og_image']

def run():
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        name = os.path.basename(f)
        if name.startswith(('_', 'v2-')): continue
        t = open(f).read()
        t = re.sub(r'\n?<!--seo-->.*?<!--/seo-->', '', t, flags=re.S)
        t = re.sub(r'<meta name="robots" content="[^"]*">\n?', '', t)
        title = strip(re.search(r'<title>(.*?)</title>', t, re.S).group(1))
        ov = S.get('pages', {}).get(name, {})
        desc = ov.get('description') or describe(t); img = ov.get('image') or og_image(t, name)
        url = S['url'] + ('' if name == 'index.html' else name)
        robots = 'noindex, nofollow' if S.get('noindex') else 'index, follow'
        block = f'''<!--seo--><meta name="robots" content="{robots}">
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="32x32"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(S['name'])}"><meta property="og:locale" content="uk_UA">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{e(S['url'] + img)}"><meta name="twitter:card" content="summary_large_image"><!--/seo-->'''
        t = t.replace('</title>', '</title>\n' + block, 1)
        open(f, 'w').write(t); n += 1
    print('seo:', n, 'pages;', 'noindex' if S.get('noindex') else 'index', S['url'])

if __name__ == '__main__':
    run()
