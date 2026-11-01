#!/usr/bin/env python3
"""Медіа для сторінок моделей (запуск на сервері):
  python3 build/media.py gallery  — до 5 ракурсів кожної моделі → img/hd/<модель>-g1..g5.webp (у git)
  python3 build/media.py video    — вступне відео моделі/серії з Google Drive, стиснене до 720p → video/<ключ>.mp4 + .jpg (поза git)
Результат описується в content/catalog/media.json."""
import json, re, io, os, sys, subprocess, tempfile
sys.path.insert(0, '/root/gd'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import make_dl, fetch, api
from dlr import make_dlr, fetch_file
from PIL import Image
from hd_images import OV, slug, models
Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MJ = os.path.join(ROOT, 'content/catalog/media.json')
media = json.load(open(MJ)) if os.path.exists(MJ) else {}
save = lambda: json.dump(media, open(MJ, 'w'), ensure_ascii=False, indent=1)
# main-image overrides (file name fragment)
MAIN = {'AT101': 'tracker-fro', 'UC100': 'controller-front', 'UC701': 'UC701 (2)', 'TS60x': 'TS601 (16)', 'WS301': 'WS301 (3)', 'EM320-TILT': 'tilt-3'}
# video folder per model (suffix of path under "8 Video/"), first match wins
VID = {'AM102/AM102L': 'AM Series/AM Series', 'AM103/AM103L': 'AM103 & AM130L/Introduction', 'AM300 Series': 'AM307 & AM319/Introduction',
 'CT10x': 'CT1xx & CT3xx/Series Intro', 'CT3xx': 'CT1xx & CT3xx/Series Intro', 'CTH01': 'CT Series/CTH01', 'WS156': 'CoWork Series/WS156', 'WS201': 'CoWork Series/WS201',
 'WS203': 'CoWork Series/WS203', 'WS302': 'CoWork Series/WS302', 'WS303': 'CoWork Series/WS303', 'WS50x': 'CoWork Series/WS50x', 'WS558': 'CoWork Series/WS558',
 'WS101': 'Solution & Kit/CoWork Smart Office Solution', 'WS202': 'Solution & Kit/CoWork Smart Office Solution', 'WS301': 'Solution & Kit/CoWork Smart Office Solution',
 'WS51x': 'Solution & Kit/CoWork Smart Office Solution', 'WS523': 'Solution & Kit/CoWork Smart Office Solution',
 'EM300-CL': 'EM300 Series/EM300-CL', 'EM300-MLD': 'EM300 Series/EM300-MLD', 'EM320-TH': 'EM300 Series/EM320-TH', 'EM320-TILT': 'EM300 Series/EM320-TILT',
 'EM300-TH': 'Solution & Kit/Temperature and Humidity Monitoring Solution', 'EM300-DI': 'Solution & Kit/Smart Water Management in Building',
 'EM300-SLD/ZLD': 'Solution & Kit/Smart Water Management in Building', 'EM300-MCS': 'Solution & Kit/CoWork Smart Office Solution',
 'EM400-MUD': 'EM400 Series/EM400 Series Distance Level Measuring Sensors', 'EM400-TLD': 'EM400 Series/EM400 Series Distance Level Measuring Sensors',
 'EM400-UDL': 'EM400 Series/EM400 Series Distance Level Measuring Sensors', 'EM410-RDL': 'EM400 Series/EM410-RDL Radar Distance_Level Sensor',
 'EM500-CO2': 'EM500 Series/EM500 Series', 'EM500-LGT': 'EM500 Series/EM500 Series', 'EM500-PP': 'EM500 Series/EM500 Series', 'EM500-PT100': 'EM500 Series/EM500-PT100',
 'EM500-SMTC': 'EM500 Series/EM500-SMT', 'EM500-SWL': 'EM500 Series/EM500-SWL', 'EM500-UDL': 'EM500 Series/EM500-UDL',
 'GS301': 'GS Series/GS301 LoRaWAN® Bathroom Odor Detector', 'GS601': 'GS Series/GS601 Vape Detector', 'TS101': 'TS Series/TS101 Insertion Temperature Sensor',
 'TS201': 'TS Series/TS201', 'TS301/TS302': 'TS Series/TS30x', 'TS60x': 'TS Series/TS60x', 'VS121': 'VS Series/VS121/Introduction', 'VS125 Series': 'VS Series/VS125 & VS126/VS125',
 'VS126': 'VS Series/VS125 & VS126', 'VS133': 'VS Series/VS133/Product Introduction', 'VS135': 'VS Series/VS135', 'VS330': 'VS Series/VS330', 'VS340/VS341': 'VS Series/VS34x',
 'VS350': 'VS Series/VS350', 'VS351': 'VS Series/VS351/Introduction', 'VS360': 'VS Series/VS360', 'VS370': 'VS Series/VS370', 'VS373': 'VS Series/VS373',
 'WT10x': 'WT Series/WT101/Introduction Video', 'WT2x1': 'WT Series/WT201', 'WT30x': 'WT Series/WT303&WT304', 'WTS506': 'Sensor & Node/WTS Series', 'AT101': 'AT Series/AT101 Outdoor Asset Tracker',
 'DS3604': 'IoT Display/DS3604', 'EG71': 'Gateway/EG71', 'SG50': 'Gateway/SG50', 'UG56': 'Gateway/UG56', 'UG63': 'Gateway/UG63', 'UG65': 'Gateway/UG65', 'UG67': 'Gateway/UG67',
 'UC100': 'UC100/Introduction', 'UC300': 'IoT Controller/UC300', 'UC51x': 'IoT Controller/UC51x'}
def renders():
    rs = [json.loads(l) for l in open('/root/gd/photo_captions.jsonl')]
    return [r for r in rs if 'Rendered Image/' in r['path'] and (r.get('caption') or {}).get('type') == 'рендер' and r['path'].lower().endswith('.png')]
def cls(a):
    a = a.lower()
    for k, p in [('back', r'ззаду|задн|тильн|back'), ('bottom', r'знизу|bottom'), ('top', r'зверху|top'), ('side', r'бічн|профіл|side|left|right|збоку'), ('34', r'3/4|ізометр|три чверт|трикутн|під кутом|three'), ('front', r'фронт|спереду|front')]:
        if re.search(p, a): return k
    return 'other'
def gallery():
    rs = renders(); OUT = os.path.join(ROOT, 'img/hd/')
    junk = re.compile(r'упаков|комплект|детал|кріпл|аксесуар|кабел|зонд|probe|package|box', re.I)
    wid, path = make_dl()
    try:
        for m in models():
            s = slug(m); f = OV.get(m, m)
            c = [r for r in rs if r['path'].split('Rendered Image/')[1].rsplit('/', 1)[0].endswith(f) and not junk.search(str(r['caption'].get('angle', '')) + ' ' + r['path'].split('/')[-1])]
            c.sort(key=lambda r: -r['size'])
            if MAIN.get(m):
                c.sort(key=lambda r: 0 if MAIN[m] in r['path'] else 1)
            order = ['front', '34', 'side', 'back', 'top', 'other', 'bottom']; pick = []; seen = set()
            if MAIN.get(m) and c and MAIN[m] in c[0]['path']: pick.append(c[0]); seen.add(cls(str(c[0]['caption'].get('angle', '')) + ' ' + c[0]['path'].split('/')[-1]))
            for k in order:
                for r in c:
                    if len(pick) >= 5: break
                    if r in pick: continue
                    if cls(str(r['caption'].get('angle', '')) + ' ' + r['path'].split('/')[-1]) == k and k not in seen: pick.append(r); seen.add(k); break
            for r in c:
                if len(pick) >= 4: break
                if r not in pick: pick.append(r)
            files = []
            for i, r in enumerate(pick[:5], 1):
                fn = '%s-g%d.webp' % (s, i)
                try:
                    if not os.path.exists(OUT + fn):
                        im = Image.open(io.BytesIO(fetch(path, r['id']))).convert('RGBA')
                        bb = im.split()[3].point(lambda v: 255 if v > 12 else 0).getbbox(); im = im.crop(bb) if bb else im
                        im.thumbnail((900, 900)); im.save(OUT + fn, 'WEBP', quality=84)
                    files.append('img/hd/' + fn)
                except Exception as e: print('ERR', m, e, flush=True)
            if MAIN.get(m) and files:  # main thumbnail = first gallery image
                Image.open(os.path.join(ROOT, files[0])).copy().save(OUT + s + '.webp', 'WEBP', quality=86)
            media.setdefault(m, {})['gallery'] = files; save(); print('gallery', m, len(files), flush=True)
    finally:
        api('DELETE', '/workflows/%s' % wid)
def video():
    vs = [json.loads(l) for l in open('/root/gd/video_captions.jsonl')]
    VD = os.path.join(ROOT, 'video/'); os.makedirs(VD, exist_ok=True)
    wid, path = make_dlr(); done = {}
    try:
        for m in models():
            f = VID.get(m)
            if not f: continue
            c = [v for v in vs if v['path'].split('8 Video/')[-1].rsplit('/', 1)[0].endswith(f) and v['path'].lower().endswith(('.mp4', '.mov'))]
            c.sort(key=lambda v: (0 if v.get('has_subtitles') else 1, -v['size']))
            if not c: print('NOVIDEO', m, flush=True); continue
            v = c[0]; key = done.get(v['id'])
            if not key:
                key = re.sub(r'[^a-z0-9]+', '-', v['path'].split('/')[-1].rsplit('.', 1)[0].lower()).strip('-')[:60]
                mp4 = VD + key + '.mp4'
                if not os.path.exists(mp4):
                    with tempfile.NamedTemporaryFile(suffix='.src', dir='/root/gd') as t:
                        fetch_file(path, v['id'], v['size'], t.name)
                        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', t.name, '-vf', 'scale=-2:min(720\\,ih)', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '28',
                                        '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', mp4], check=True)
                    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(min(5, v['duration_s'] // 3)), '-i', mp4, '-frames:v', '1', '-q:v', '4', VD + key + '.jpg'], check=True)
                done[v['id']] = key
            media.setdefault(m, {})['video'] = {'src': 'video/' + key + '.mp4', 'poster': 'video/' + key + '.jpg', 'title': v['path'].split('/')[-1].rsplit('.', 1)[0].replace('_', ' '), 'dur': v['duration_s']}
            save(); print('video', m, key, os.path.getsize(VD + key + '.mp4') // 1000000, 'MB', flush=True)
    finally:
        api('DELETE', '/workflows/%s' % wid)
if __name__ == '__main__':
    {'gallery': gallery, 'video': video}[sys.argv[1]]()
