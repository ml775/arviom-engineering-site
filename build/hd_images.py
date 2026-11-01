#!/usr/bin/env python3
"""Підбирає великі рендери продуктів з Google Drive (опис фото /root/gd/photo_captions.jsonl) → img/hd/<модель>.webp.
Запуск на сервері: python3 build/hd_images.py"""
import json, re, io, os, sys
sys.path.insert(0, '/root/gd')
from dl import make_dl, fetch, api
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'img/hd/'); os.makedirs(OUT, exist_ok=True)
OV = {'AM102/AM102L':'AM102(L)/AM102','AM103/AM103L':'AM103(L)/AM103','AM300 Series':'AM Series/AM308','VS121':'VS121/VS121/White','VS125 Series':'VS Series/VS125',
'VS126':'VS126/VS126 front','VS133':'VS133/White Version','VS135':'VS135/White','VS340/VS341':'VS34x/VS340','VS351':'VS351/VS351 Battery Version','VS360':'VS360/VS360 White Transmistter',
'WT10x':'WT Series/WT101','WT2x1':'WT201/WT201 Without Mounting Kit','WT30x':'WT Series/WT303 & WT304','WT401':'WT401/WT401','UC711 + WT401':'4 Controller/UC711',
'WS156':'WS136 & 156/WS156','WS50x':'WS50x/WS502EU','WS51x':'WS51x/Type-F','WS523':'WS523/Standard/European Standard','WS558':'WS558/Switch','WS101':'WS101/WS101',
'TS60x':'TS60x/TS601','TS201':'TS201/With probe','TS301/TS302':'TS301/TS302/TS301','EM300-SLD/ZLD':'EM300-SLD','EM320-TH':'EM320-TH/Cable Tie Version',
'EM400-UDL':'EM400-UDL/EM400-UDL(W050/W100/S050)','CT10x':'CT101/CT101 Standard','CT3xx':'CT Series/CT305','UC50x':'UC50x/UC501','UC51x':'UC51x/UC511','CTH01':'CT Series/CTH01'}
slug = lambda m: re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', m.lower()))
def models():
    C = os.path.join(ROOT, 'content/catalog/')
    s = json.load(open(C + 'sensor_series.json')); c = json.load(open(C + 'iot_catalog.json')); m = []
    for x in s: m += [p['model'] for p in x['products'] if p['model'] != 'Compatibility']
    for k in ['lorawan-gateway', 'lorawan-controller', 'iot-display']: m += [x['title'][0] for x in c[k]['products']]
    return list(dict.fromkeys(m))
if __name__ == '__main__':
    rs = [json.loads(l) for l in open('/root/gd/photo_captions.jsonl')]
    rs = [r for r in rs if 'Rendered Image/' in r['path'] and (r.get('caption') or {}).get('type') == 'рендер' and r['path'].lower().endswith('.png')]
    good = re.compile(r'фронт|3/4|ізометр|спереду|front', re.I)
    bad = re.compile(r'знизу|ззаду|задн|монтажн|тильн|бічн|профіл|left|right|side|ракурс справа|ракурс зліва|торцев|bottom|back|botton|top|зверху|кріпл|детал|упаков|комплект', re.I)
    sel = {}
    for m in models():
        if os.path.exists(OUT + slug(m) + '.webp'): continue
        f = OV.get(m, m)
        c = [r for r in rs if r['path'].split('Rendered Image/')[1].rsplit('/', 1)[0].endswith(f)]
        key = lambda r: str(r['caption'].get('angle', '')) + ' ' + r['path'].split('/')[-1]
        c.sort(key=lambda r: (1 if bad.search(key(r)) else 0, 0 if good.search(key(r)) else 1, 0 if 'проз' in str(r['caption'].get('background', '')) else 1, -r['size']))
        if c: sel[m] = c[0]
        else: print('NONE', m, flush=True)
    wid, path = make_dl()
    try:
        for m, r in sel.items():
            try:
                im = Image.open(io.BytesIO(fetch(path, r['id']))).convert('RGBA')
                bb = im.split()[3].point(lambda v: 255 if v > 12 else 0).getbbox(); im = im.crop(bb) if bb else im
                im.thumbnail((640, 640)); im.save(OUT + slug(m) + '.webp', 'WEBP', quality=86)
                print('ok', m, im.size, r['path'].split('/')[-1], flush=True)
            except Exception as e: print('ERR', m, e, flush=True)
    finally:
        api('DELETE', '/workflows/%s' % wid)
