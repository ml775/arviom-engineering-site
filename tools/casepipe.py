"""Кейси Milesight → дані для сайту. Запуск на VPS: python3 casepipe.py <url> [<url>...]
Результат: /root/gd/cases/out/<slug>/case.json + *.webp"""
import sys, os, re, json, html, io, urllib.request, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
OUT = '/root/gd/cases/out'
UA = {'User-Agent': 'Mozilla/5.0'}
AK = subprocess.check_output(['docker', 'exec', 'energy-dashboard', 'printenv', 'ANTHROPIC_API_KEY']).decode().strip()

def get(u, binary=False):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    return r if binary else r.decode('utf-8', 'ignore')

def text_of(h):
    t = re.sub(r'(?s)<(script|style|noscript|header|footer|nav|svg)[^>]*>.*?</\1>', ' ', h)
    t = re.sub(r'(?i)<h[1-4][^>]*>', '\n## ', t); t = re.sub(r'(?i)<li[^>]*>', '\n- ', t); t = re.sub(r'(?i)<(p|div|br)[^>]*>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t)); t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r'\n\s*\n+', '\n', t)
    cut = re.search(r'(?i)which area are you interested|discover more about milesight products', t)
    return t[:cut.start()] if cut else t

def images(h, slug, url):
    from collections import Counter
    found = re.findall(r'[^"\'( ,<>]*\.(?:jpg|jpeg|png|webp)', h)
    folders = Counter(x.rsplit('/', 1)[0] for x in found if '/success-stories/' in x and slug[:12] in x)
    if not folders:
        folders = Counter(x.rsplit('/', 1)[0] for x in found if '/success-stories/' in x)
    own = folders.most_common(1)[0][0] if folders else ''
    if not own:
        part = 'iot' if '/iot/' in url else 'company'
        own = f'/static/pc/en/{part}/success-stories/{slug}'
    keep = []
    for x in found:
        if '/' not in x: x = own + '/' + x
        if x.rsplit('/', 1)[0] != own and 'wp-content/uploads' not in x: continue
        if re.search(r'(?i)(discover-more|partner|why-choose|logo|icon|/nav/|footer)', x): continue
        if x.startswith('/'): x = 'https://www.milesight.com' + x
        if x not in keep: keep.append(x)
    return keep

def claude(prompt, model='claude-sonnet-5-5'):
    body = {'model': model, 'max_tokens': 6000, 'messages': [{'role': 'user', 'content': prompt}]}
    r = urllib.request.Request('https://api.anthropic.com/v1/messages', data=json.dumps(body).encode(),
        headers={'x-api-key': AK, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
    d = json.load(urllib.request.urlopen(r, timeout=300))
    return ''.join(b.get('text', '') for b in d['content'])

SCHEMA = '''Поверни ЛИШЕ JSON (без ``` і пояснень) такої форми:
{"dir": "energy|building|industry|air|water|agro",
 "obj": "тип об'єкта коротко, 1-2 слова, напр. Офісні будівлі / Житлові будинки / Готелі / Лікарні / Школи / Рітейл / Заводи / Аеропорти / Водоканал / Ферми / Теплиці",
 "country": "країна українською", "place": "країна, місто або об'єкт, коротко",
 "title": "заголовок картки: результат + об'єкт, з цифрою якщо є, до 90 знаків",
 "text": "1-2 речення для картки",
 "devices": "моделі Milesight через кому, без кількостей",
 "page": {"h1": "заголовок сторінки", "sub": "1 речення-підзаголовок",
   "facts": [["Партнер-інтегратор","назва (країна) або —"],["Локація","..."],["Обладнання","МОДЕЛЬ × кількість, ... (кількість лише якщо є в тексті)"],["Застосування","2-3 слова через ·"]],
   "background": {"text": ["абзац 1", "абзац 2"]},
   "challenges": [{"icon":"nature|tools|system","t":"назва групи","items":["...","..."]}],
   "solution": [{"t":"назва","d":"2-3 речення з конкретикою: моделі, діапазони, інтерфейси"}],
   "results": {"items": [["заголовок","1-2 речення"]], "note": "необов'язково"},
   "partner": "1-2 речення про партнера або порожньо",
   "hero": "файл для головного банера: найширше ФОТО об'єкта або банер (у назві часто banner/background/header), не схема і не скриншот",
   "bg_img": "файл фото для блоку передумов",
   "solution_img": "файл схеми/топології рішення або порожньо",
   "results_img": "файл скриншота платформи/графіка або порожньо"}}
У кожному блоці solution додай "imgs": [1-2 файли з переліку, що найкраще ілюструють блок, ширина від 400 px]. Файли бери ЛИШЕ з переліку ЗОБРАЖЕННЯ, не повторюй один файл у різних місцях.'''

RULES = '''Ти пишеш кейс для сайту українського дистриб'ютора Milesight. Мова — українська. Пиши своїми словами, стисло, по-інженерному, без реклами, без перекладу дослівно.
Використовуй ЛИШЕ факти з тексту нижче: цифри, моделі, кількості, назви — тільки якщо вони є в тексті. Нічого не вигадуй. Якщо партнера немає — "—".
challenges: 2-3 групи по 2-3 пункти (icon: nature — природа/середовище, tools — інфраструктура/обладнання, system — керування/процеси).
solution: 2-4 блоки, по одному на підсистему. results: рівно 4 пункти, якщо в тексті є цифри результату — обов'язково включи.
dir: energy — облік енергії, освітлення, енергоефективність; building — BMS, опалення, HVAC, керування будівлею; industry — заводи, обладнання; air — якість повітря; water — вода, протічки, паводки; agro — сільське господарство, теплиці, ліси.'''

def run(url):
    slug = url.rstrip('/').split('/')[-1]; d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True)
    h = get(url); t = text_of(h); open(os.path.join(d, 'text.txt'), 'w').write(t)
    imgs = []
    for i, u in enumerate(images(h, slug, url)):
        try:
            im = Image.open(io.BytesIO(get(u, True))).convert('RGB')
        except Exception as e:
            continue
        name = re.sub(r'[^a-z0-9-]+', '-', os.path.splitext(u.split('/')[-1])[0].lower())[:50] + '.webp'
        w, hh = im.size
        if w > 2000: im.thumbnail((2000, 2000))
        im.save(os.path.join(d, name), 'WEBP', quality=86); imgs.append({'file': name, 'w': w, 'h': hh, 'url': u})
    banner = [x for x in imgs if 'banner' in x['file'] or x['w'] >= 1600]
    lst = '\n'.join(f"{x['file']} {x['w']}x{x['h']}" for x in imgs if x['w'] >= 200)
    raw = claude(RULES + '\n\n' + SCHEMA + '\n\nЗОБРАЖЕННЯ (файл ширина x висота):\n' + lst + '\n\nТЕКСТ КЕЙСУ:\n' + t[:24000])
    m = re.search(r'\{.*\}', raw, re.S); c = json.loads(m.group(0))
    c['link'] = url; c['slug'] = slug; c['images'] = imgs; c['hero_file'] = banner[0]['file'] if banner else (max(imgs, key=lambda x: x['w'])['file'] if imgs else '')
    json.dump(c, open(os.path.join(d, 'case.json'), 'w'), ensure_ascii=False, indent=1)
    print(slug, c['dir'], len(imgs), 'imgs', c['hero_file'], c['title'][:60])

if __name__ == '__main__':
    for u in sys.argv[1:]:
        try: run(u)
        except Exception as e: print('FAIL', u, e)
