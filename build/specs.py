#!/usr/bin/env python3
"""Витягує характеристики моделей з даташитів у базі знань (kb-db) через Claude API.
Запуск на сервері: python3 build/specs.py  → content/catalog/specs.json (докачує відсутні)."""
import json, os, sys, subprocess, urllib.request, concurrent.futures as cf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/root/gd'); from cap import AK
OUT = os.path.join(ROOT, 'content/catalog/specs.json')
P = ("З даташиту Milesight витягни характеристики моделі {m}. Відповідай ЛИШЕ JSON, значення українською, коротко, як у таблиці. "
     "Якщо даних немає — порожній рядок або []. Ключі: "
     '{{"model":"{m}","name_uk":коротка назва,"purpose":для чого (1 речення),"measures":[що вимірює або чим керує],'
     '"range_accuracy":діапазон і точність коротко,"probe":сенсор/зонд/технологія,"interfaces":входи-виходи й порти,'
     '"network":зв\'язок (LoRaWAN клас, 4G, Ethernet, Wi-Fi тощо),"power":живлення,"battery":батарея,"battery_life":термін роботи від батареї,'
     '"ip":ступінь захисту,"temp":робоча температура,"dimensions":розміри,"weight":вага,"mounting":монтаж,"range_lora":дальність зв\'язку,'
     '"config":налаштування,"storage":зберігання даних,"frequencies":частотні плани,"highlights":[3 ключові переваги коротко]}}')
def doc(i):
    return subprocess.check_output(['docker', 'exec', 'kb-db', 'psql', '-U', 'kb', '-d', 'kb', '-Atc', 'select content from raw_docs where id=%d' % i]).decode()[:30000]
def one(model, ids):
    text = '\n\n---\n\n'.join(doc(i) for i in ids)
    body = {"model": "claude-sonnet-5-5", "max_tokens": 3000, "thinking": {"type": "between_tools"},
            "messages": [{"role": "user", "content": P.format(m=model) + "\n\n" + text}]}
    r = urllib.request.Request('https://api.anthropic.com/v1/messages', data=json.dumps(body).encode(),
        headers={'x-api-key': AK, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
    d = json.load(urllib.request.urlopen(r, timeout=240))
    t = ''.join(b.get('text', '') for b in d['content'] if b.get('type') == 'text').strip()
    if t.startswith('```'): t = t.strip('`').split('\n', 1)[1].rsplit('```', 1)[0]
    j = json.loads(t); j['model'] = model; j['_src'] = ids; return j
if __name__ == '__main__':
    mp = json.load(open(os.path.join(ROOT, 'content/catalog/ds_map.json')))
    have = json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo = {m: ids for m, ids in mp.items() if m not in have}
    print('todo', len(todo), flush=True)
    with cf.ThreadPoolExecutor(4) as ex:
        fs = {ex.submit(one, m, ids): m for m, ids in todo.items()}
        for f in cf.as_completed(fs):
            m = fs[f]
            try: have[m] = f.result(); print('ok', m, flush=True)
            except Exception as e: print('ERR', m, e, flush=True)
            json.dump(have, open(OUT, 'w'), ensure_ascii=False, indent=1)
    print('done', len(have), flush=True)
