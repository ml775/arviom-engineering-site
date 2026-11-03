#!/usr/bin/env python3
"""Імпорт кейсів, підготовлених casepipe.py на сервері.
Запуск: python3 build/import_cases.py <тека з підтеками slug/case.json + *.webp>"""
import json, os, sys, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1]
P = os.path.join(ROOT, 'content/cases.json'); D = json.load(open(P))
have = {c['link'].rstrip('/').split('/')[-1]: c for c in D['ms']}
for slug in sorted(os.listdir(src)):
    f = os.path.join(src, slug, 'case.json')
    if not os.path.exists(f): continue
    c = json.load(open(f)); pg = c['page']
    old = have.get(slug)
    if old and old.get('page'): print('skip', slug); continue
    if old: D['ms'].remove(old); print('replace', slug)  # старий запис без сторінки → повний
    dst = os.path.join(ROOT, 'img/cases', slug); os.makedirs(dst, exist_ok=True)
    def im(name):
        if not name: return ''
        s = os.path.join(src, slug, name)
        if not os.path.exists(s): return ''
        shutil.copy(s, os.path.join(dst, name)); return f'img/cases/{slug}/{name}'
    hero = im(pg.get('hero') or c.get('hero_file'))
    sol = [{'t': x['t'], 'd': x['d'], 'imgs': [p for p in (im(i) for i in x.get('imgs', [])) if p]} for x in pg['solution']]
    page = {'slug': 'case-' + slug[:60], 'h1': pg['h1'], 'sub': pg['sub'], 'hero': hero,
            'facts': pg['facts'], 'background': {'text': pg['background']['text'], 'img': im(pg.get('bg_img'))},
            'challenges': pg['challenges'], 'solution': sol,
            'results': {'items': pg['results']['items'], 'note': pg['results'].get('note', ''), 'img': im(pg.get('results_img'))},
            'partner': pg.get('partner', '')}
    if pg.get('solution_img'):
        page['solution_img'] = im(pg['solution_img']); page['solution_caption'] = 'Схема рішення — Milesight.'
    card_img = page['background']['img'] or hero
    D['ms'].append({'dir': c['dir'], 'title': c['title'], 'place': c['place'], 'text': c['text'], 'devices': c.get('devices', ''),
                    'image': card_img, 'link': c['link'], 'obj': c['obj'], 'country': c['country'], 'page': page})
    print('added', slug, c['dir'])
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=2); open(P, 'a').write('\n')

# превью для плашок — як на milesight.com (див. build/ms_cards.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ms_cards; ms_cards.main()
