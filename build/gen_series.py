#!/usr/bin/env python3
"""Генерує сторінки серій s-<серія>.html з шаблону build/series_tpl.html.
Дані: content/catalog/sensor_series.json, iot_catalog.json (склад серій, фото),
content/catalog/specs.json (характеристики з даташитів), data.js (серія EM300)."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
from uk import UK
C = os.path.join(ROOT, 'content/catalog/')
ser = {s['key']: s for s in json.load(open(C + 'sensor_series.json'))}
cat = json.load(open(C + 'iot_catalog.json'))
specs = json.load(open(C + 'specs.json')) if os.path.exists(C + 'specs.json') else {}
img = lambda n: 'img/cat/cat-' + n.split('?')[0].split('/')[-1].rsplit('.', 1)[0] + '.webp'
slug = lambda m: re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', m.lower()))
SENS = [["measures", "Вимірює"], ["battery_life", "Батарея"], ["ip", "Захист"]]
NET = [["network", "Зв'язок"], ["power", "Живлення"], ["ip", "Захист"]]
SERIES = {
 'am-series': ('AM', 'Серія AM', 'Датчики якості повітря в приміщенні', 'Від двох до дев\'яти параметрів повітря: CO₂, температура, вологість, PM2.5/PM10, TVOC — з екраном або без.', SENS),
 'occupancy-and-people-counting-series': ('VS', 'Присутність і люди', 'Присутність, зайнятість і підрахунок людей', 'Датчики присутності, зайнятості місць і лічильники відвідувачів: ToF, стереозір, радар, термопара.', SENS),
 'wt-series': ('WT', 'Серія WT', 'Термостати й керування опаленням', 'Термостати радіаторів, фанкойлів і систем HVAC з керуванням по LoRaWAN.', SENS),
 'gs-series': ('GS', 'Серія GS', 'Датчики запаху й вейпу', 'Контроль запахів у санвузлах і виявлення вейпу.', SENS),
 'cowork-series': ('WS', 'Серія CoWork', 'Розумний офіс без кабелів', 'Кнопки, вимикачі, розетки, датчики руху, шуму, протічки й відкриття.', SENS),
 'wts-series': ('WTS', 'Серія WTS', 'IoT-метеостанція', 'Вуличні метеодані для агро, міста й будівництва.', SENS),
 'ts-series': ('TS', 'Серія TS', 'Датчики температури', 'Температура в холодильниках, на складах, в аптеках і під час перевезення.', SENS),
 'em400-series': ('EM400', 'Серія EM400', 'Відстань і рівень', 'Лазерні, ультразвукові й радарні датчики рівня та відстані: баки, контейнери, паркування.', SENS),
 'em500-series': ('EM500', 'Серія EM500', 'Промислові датчики', 'Тиск у трубах, температура PT100, CO₂, освітленість, ґрунт і рівень води — для вулиці й промисловості.', SENS),
 'at-series': ('AT', 'Серія AT', 'GPS-трекери', 'Вуличний трекер для обладнання й транспорту.', SENS),
 'ct-series': ('CT', 'Серія CT', 'Струм і енергія', 'Трансформатори струму й хаб енергомоніторингу щита без розриву ліній.', SENS),
 'iot-display': ('DS', 'IoT-дисплей', 'E-ink дисплей LoRaWAN', 'Табло для переговорних, складів і цехів, що працює від батареї.', SENS),
}
OTHER = {'gateways': ('lorawan-gateway', 'UG', 'LoRaWAN-шлюзи', 'Шлюзи для приміщень і вулиці', 'Збирають дані з датчиків і передають у вашу систему: MQTT, HTTP, Modbus, BACnet.', NET),
         'controllers': ('lorawan-controller', 'UC', 'LoRaWAN-контролери', 'Контролери й конвертери', 'Підключають наявне обладнання: лічильники Modbus, реле, клапани, кондиціонери.', NET)}
FILE = {k: 's-' + k.replace('-series', '').replace('occupancy-and-people-counting', 'people') + '.html' for k in list(SERIES) + list(OTHER)}
FILE['em300-series'] = 'catalog.html'

def model(m, name, im, href):
    d = {'model': m, 'name_uk': UK.get(name, name), 'img': img(im), 'ext': ('https://www.milesight.com' + href) if href.startswith('/') else href, 'specs': False}
    s = specs.get(m)
    if s:
        d.update({k: v for k, v in s.items() if not k.startswith('_') and k != 'model'}); d['specs'] = True
        d['name_uk'] = UK.get(name, name)
    return d

def page(key, S, models, cases=None):
    tpl = open(os.path.join(ROOT, 'build/series_tpl.html')).read()
    data = 'const MODELS=%s;\nconst CASES=%s;\nconst S=%s;' % (json.dumps(models, ensure_ascii=False), json.dumps(cases or [], ensure_ascii=False), json.dumps(S, ensure_ascii=False))
    act = {'__A_SENS__': '', '__A_GW__': '', '__A_CTL__': ''}
    act['__A_GW__' if key == 'gateways' else '__A_CTL__' if key == 'controllers' else '__A_SENS__'] = ' aria-current="page"'
    for k, v in act.items(): tpl = tpl.replace(k, v)
    out = tpl.replace('__TITLE__', S['title']).replace('__DATA__', data, 1)
    open(os.path.join(ROOT, FILE[key]), 'w').write(out)
    return FILE[key], sum(m['specs'] for m in models), len(models)

if __name__ == '__main__':
    res = []
    for key, (code, title, sub, text, card) in SERIES.items():
        ms = [model(p['model'], p['name'], p['img'], p['href']) for p in ser[key]['products'] if p['model'] != 'Compatibility']
        res.append(page(key, {'code': code, 'title': title, 'sub': sub, 'text': text, 'card': card}, ms))
    for key, (src, code, title, sub, text, card) in OTHER.items():
        ms = [model(x['title'][0], ' '.join(x['title'][1:]), x['img'], x['href'].replace('https://www.milesight.com', '')) for x in cat[src]['products']]
        res.append(page(key, {'code': code, 'title': title, 'sub': sub, 'text': text, 'card': card}, ms))
    # EM300: curated data from data.js
    js = open(os.path.join(ROOT, 'data.js')).read()
    M = json.loads(re.search(r'const MODELS=(\[.*?\]);', js, re.S).group(1)); CASES = json.loads(re.search(r'const CASES=(\[.*?\]);', js, re.S).group(1))
    for m in M: m['img'] = 'img/' + m['model'].lower() + '.webp'; m['specs'] = True
    S = {'code': 'EM300', 'title': 'Серія EM300', 'sub': 'Серія компактних датчиків LoRaWAN',
         'text': 'Один корпус і одна логіка налаштування — різні сенсори: клімат, протікання, двері, імпульсні лічильники, рівень і нахил.',
         'facts': [['IP67', 'корпус для вулиці й підвалу'], ['до 10 р.', 'від батареї*'], ['NFC', 'налаштування телефоном']],
         'footnote': '* Ресурс залежить від інтервалу передачі й умов; точні цифри — у порівнянні та на сторінці моделі.',
         'groups': [["all","Усі"],["clim","Клімат"],["leak","Протікання"],["door","Двері й вікна"],["pulse","Імпульси й облік"],["level","Рівень рідини"],["tilt","Нахил"]],
         'group_of': {"EM300-TH":"clim","EM320-TH":"clim","EM300-MCS":"door","EM300-DI":"pulse","EM300-CL":"level","EM300-SLD":"leak","EM300-ZLD":"leak","EM300-MLD":"leak","EM320-TILT":"tilt"},
         'cases_for': ['EM300-TH', 'EM320-TH']}
    res.append(page('em300-series', S, M, CASES))
    json.dump(FILE, open(C + 'series_files.json', 'w'), ensure_ascii=False, indent=0)
    for r in res: print('%-18s specs %d/%d' % r)
