#!/usr/bin/env python3
"""Картки кейсів Milesight: беремо превью зі сторінки списку milesight.com (як у них на плашках).
Запуск: python3 build/ms_cards.py  → img/cases/<slug>/card.webp + поле image в content/cases.json"""
import io, json, os, re, urllib.request
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST = 'https://www.milesight.com/company/success-stories'

def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()

def thumbs():
    h = get(LIST).decode('utf-8', 'ignore'); out = {}
    for a in re.finditer(r'<a[^>]+href="([^"]*success-stories/[^"#?]+)"(.*?)</a>', h, re.S):
        m = re.search(r'(?:data-src|data-original|src)="([^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"', a.group(2))
        if m:
            out.setdefault(a.group(1).rstrip('/').split('/')[-1], m.group(1))
    return out

def main():
    p = os.path.join(ROOT, 'content/cases.json'); d = json.load(open(p)); T = thumbs(); n = 0
    for c in d['ms']:
        slug = c['link'].rstrip('/').split('/')[-1]; u = T.get(slug)
        if not u:
            print('нема превью:', slug); continue
        u = u if u.startswith('http') else 'https://www.milesight.com' + ('' if u.startswith('/') else '/') + u
        im = Image.open(io.BytesIO(get(u))).convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3])
        dst = f'img/cases/{slug}'; os.makedirs(os.path.join(ROOT, dst), exist_ok=True)
        bg.save(os.path.join(ROOT, dst, 'card.webp'), 'WEBP', quality=90); c['image'] = f'{dst}/card.webp'; n += 1
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); print('картки:', n, 'з', len(d['ms']))

if __name__ == '__main__':
    main()
