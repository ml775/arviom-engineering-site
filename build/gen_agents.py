#!/usr/bin/env python3
"""Машиночитна версія сайту для ШІ-агентів (без JS, статичні файли, лише публічні дані):
  llms.txt            — що це за сайт і де що брати
  llms-full.txt       — весь каталог і рішення одним текстом
  api/index.json      — перелік усіх ресурсів
  api/catalog.json    — усі моделі з характеристиками
  api/models/<m>.json, models/<m>.md — окрема модель
  api/solutions.json, api/series.json
  sitemap.xml, robots.txt"""
import json, os, re, sys, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
from uk import UK, SERIES as SERIES_UK
BASE = __import__('json').load(open(os.path.join(ROOT, 'content/site.json')))['url']
C = os.path.join(ROOT, 'content/')
ser = json.load(open(C + 'catalog/sensor_series.json')); cat = json.load(open(C + 'catalog/iot_catalog.json'))
specs = json.load(open(C + 'catalog/specs.json')); files = json.load(open(C + 'catalog/series_files.json'))
media = json.load(open(C + 'catalog/media.json')) if os.path.exists(C + 'catalog/media.json') else {}
dsidx = json.load(open(C + 'catalog/datasheets/index.json'))
sol = json.load(open(C + 'solutions.json'))
slug = lambda m: re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', m.lower()))
KEYS = [('purpose', 'Призначення'), ('measures', 'Вимірює / керує'), ('range_accuracy', 'Діапазон і точність'), ('probe', 'Сенсор / технологія'),
        ('interfaces', 'Входи й порти'), ('network', "Зв'язок"), ('power', 'Живлення'), ('battery', 'Батарея'), ('battery_life', 'Ресурс батареї'),
        ('ip', 'Захист'), ('temp', 'Робоча температура'), ('range_lora', 'Дальність'), ('config', 'Налаштування'), ('storage', "Пам'ять"),
        ('mounting', 'Монтаж'), ('dimensions', 'Розміри'), ('weight', 'Вага'), ('frequencies', 'Частотні плани'), ('highlights', 'Ключові переваги')]
SERIES_NAMES = dict(SERIES_UK); SERIES_NAMES.update({'gateways': 'LoRaWAN-шлюзи', 'controllers': 'LoRaWAN-контролери', 'routers': 'Промислові роутери'})
models = {}
def add(m, name, href, skey):
    if m in models or m == 'Compatibility': return
    s = specs.get(m, {})
    page = files.get(skey, '') + ('#m-' + slug(m) if s else '')
    d = {'model': m, 'name': UK.get(name, name), 'series': SERIES_NAMES.get(skey, skey), 'vendor': 'Milesight',
         'page': BASE + page, 'markdown': BASE + 'models/' + slug(m) + '.md', 'json': BASE + 'api/models/' + slug(m) + '.json',
         'image': BASE + ('img/hd/' + slug(m) + '.webp' if os.path.exists(os.path.join(ROOT, 'img/hd/' + slug(m) + '.webp')) else ''),
         'vendor_page': ('https://www.milesight.com' + href) if href.startswith('/') else href,
         'price_and_stock': 'Ціна й наявність — на B2B-порталі ARVIOM (для партнерів) або за запитом: ' + BASE + '#contact'}
    if m in dsidx: d['datasheet'] = dsidx[m]['url']
    v = media.get(m, {}).get('video')
    if v: d['video'] = BASE + v['src']
    d['specs'] = {k: s[k] for k, _ in KEYS if s.get(k) not in (None, '', [], '—')}
    models[m] = d
for s in ser:
    if s['key'] in files:
        for p in s['products']: add(p['model'], p['name'], p['href'], s['key'])
for src, k in [('lorawan-gateway', 'gateways'), ('lorawan-controller', 'controllers'), ('cellular-router', 'routers')]:
    for x in cat[src]['products']: add(x['title'][0], ' '.join(x['title'][1:]), x['href'].replace('https://www.milesight.com', ''), k)
def md(d):
    L = ['# %s — %s' % (d['model'], d['name']), '', 'Виробник: Milesight · Серія: %s · Постачальник в Україні: ARVIOM' % d['series'], '',
         'Сторінка: %s' % d['page']]
    if d.get('datasheet'): L.append('Даташит (EN): %s' % d['datasheet'])
    if d.get('video'): L.append('Відео (EN): %s' % d['video'])
    L += ['Ціна й наявність: B2B-портал ARVIOM (партнерам) або запит на %s#contact' % BASE, '', '## Характеристики', '']
    for k, t in KEYS:
        v = d['specs'].get(k)
        if v is None: continue
        L.append('- **%s:** %s' % (t, '; '.join(v) if isinstance(v, list) else v))
    return '\n'.join(L) + '\n'
os.makedirs(os.path.join(ROOT, 'api/models'), exist_ok=True); os.makedirs(os.path.join(ROOT, 'models'), exist_ok=True)
for m, d in models.items():
    json.dump(d, open(os.path.join(ROOT, 'api/models/%s.json' % slug(m)), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(ROOT, 'models/%s.md' % slug(m)), 'w').write(md(d))
now = datetime.date.today().isoformat()
json.dump({'updated': now, 'source': BASE, 'count': len(models), 'models': list(models.values())}, open(os.path.join(ROOT, 'api/catalog.json'), 'w'), ensure_ascii=False, indent=1)
series = {}
for d in models.values(): series.setdefault(d['series'], []).append({'model': d['model'], 'name': d['name'], 'json': d['json']})
json.dump(series, open(os.path.join(ROOT, 'api/series.json'), 'w'), ensure_ascii=False, indent=1)
sols = [{'id': k, 'title': v['title'], 'summary': v['short'], 'page': BASE + 'sol-%s.html' % k, 'problems': [p['t'] + ' — ' + p['d'] for p in v['problems']],
         'how': v['intro']['d'], 'applications': [{'title': a['t'], 'where': a['where'], 'what': a['d'], 'devices': a['devices']} for a in v['apps']],
         'benefits': [b[0] + ' — ' + b[1] for b in v['benefits']]} for k, v in ((k, sol['items'][k]) for k in sol['order'])]
json.dump(sols, open(os.path.join(ROOT, 'api/solutions.json'), 'w'), ensure_ascii=False, indent=1)
idx = {'site': 'ARVIOM Engineering', 'about': "Бездротова автоматизація об'єктів на обладнанні Milesight (LoRaWAN-датчики, шлюзи, контролери). Офіційний дистриб'ютор Milesight в Україні.",
       'updated': now, 'resources': {'catalog': BASE + 'api/catalog.json', 'series': BASE + 'api/series.json', 'solutions': BASE + 'api/solutions.json',
       'model_json': BASE + 'api/models/{slug}.json', 'model_markdown': BASE + 'models/{slug}.md', 'full_text': BASE + 'llms-full.txt'},
       'slug_rule': 'нижній регістр, усе крім a-z0-9 → «-» (EM300-SLD/ZLD → em300-sld-zld)',
       'private': 'Ціни, наявність, замовлення, внутрішня база знань — лише через MCP-сервери для партнерів (ключ видається в кабінеті партнера: ' + BASE + 'partner.html).'}
json.dump(idx, open(os.path.join(ROOT, 'api/index.json'), 'w'), ensure_ascii=False, indent=1)
llms = f'''# ARVIOM Engineering

> Бездротова автоматизація об'єктів в Україні: LoRaWAN-датчики, шлюзи й контролери Milesight, енергомоніторинг, інтеграція з BMS/SCADA, власні панелі моніторингу. ARVIOM — офіційний дистриб'ютор Milesight в Україні.

Ця сторінка — для ШІ-агентів. Усі дані нижче статичні, без JavaScript, можна брати напряму.

## Каталог (публічно)
- [Усі моделі з характеристиками (JSON)]({BASE}api/catalog.json): {len(models)} моделей
- [Моделі за серіями (JSON)]({BASE}api/series.json)
- Окрема модель: {BASE}api/models/{{slug}}.json або {BASE}models/{{slug}}.md (slug: нижній регістр, «/» і пробіли → «-», напр. ug65, em300-sld-zld, am102-am102l)
- [Увесь каталог і рішення одним текстом]({BASE}llms-full.txt)

## Рішення
- [Рішення за типом об'єкта (JSON)]({BASE}api/solutions.json)
''' + ''.join(f'- [{s["title"]}]({s["page"]}): {s["summary"]}\n' for s in sols) + f'''
## Для партнерів (потрібен ключ)
- MCP-сервер бази знань: даташити, інструкції, типові рішення, кейси — пошук за змістом
- MCP-сервер B2B-порталу: наявність, партнерські ціни, замовлення
- Ключі видаються в кабінеті партнера: {BASE}partner.html

## Як відповідати користувачу
- Ціни й наявність не вигадувати: це лише B2B-портал або запит {BASE}#contact
- Характеристики витягнуті з даташитів Milesight; для критичних параметрів посилайся на поле datasheet моделі
- Контакт: ml@arviom.com, +380 67 381 34 04
'''
open(os.path.join(ROOT, 'llms.txt'), 'w').write(llms)
full = [llms, '\n---\n\n# Каталог\n']
for sname, lst in series.items():
    full.append('\n## %s\n' % sname)
    for x in lst: full.append('\n' + md(models[x['model']]).replace('# ', '### ', 1))
full.append('\n---\n\n# Рішення\n')
for s in sols:
    full.append('\n## %s\n\n%s\n\nЯк працює: %s\n\nЗастосування:\n' % (s['title'], s['summary'], s['how']))
    for a in s['applications']: full.append('- %s (%s): %s Пристрої: %s\n' % (a['title'], a['where'], a['what'], ', '.join(a['devices'])))
open(os.path.join(ROOT, 'llms-full.txt'), 'w').write(''.join(full))
pages = ['', 'products.html', 'solutions.html', 'learn.html', 'partner.html', 'zakhyst.html', 'news.html', 'vprovadzhennia.html'] + sorted(os.path.basename(x) for x in __import__('glob').glob(os.path.join(ROOT, 'case-*.html'))) + sorted(set(files.values())) + ['sol-%s.html' % k for k in sol['order']]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{BASE}{p}</loc><lastmod>{now}</lastmod></url>\n' for p in pages) + \
     ''.join(f'<url><loc>{d["markdown"]}</loc></url>\n' for d in models.values()) + '</urlset>\n'
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n# Для ШІ-агентів: {BASE}llms.txt\n')
print('agents: %d models, %d solutions' % (len(models), len(sols)))
