#!/usr/bin/env python3
"""Додає даташити з content/catalog/datasheets/ у базу знань (raw_docs, processed=false — далі їх ріже й індексує kb-ingest),
прописує їх у ds_map.json і перевитягує характеристики цих моделей.
Запуск на сервері: python3 build/ingest_ds.py"""
import json, os, hashlib, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'content/catalog/datasheets/'); C = os.path.join(ROOT, 'content/catalog/')
def sql(q):
    return subprocess.check_output(['docker', 'exec', '-i', 'kb-db', 'psql', '-U', 'kb', '-d', 'kb', '-Atq', '-v', 'ON_ERROR_STOP=1'], input=q.encode()).decode().strip()
lit = lambda s: "$q$" + s.replace('$q$', '') + "$q$"
idx = json.load(open(D + 'index.json')); mp = json.load(open(C + 'ds_map.json'))
specs_path = C + 'specs.json'; specs = json.load(open(specs_path)) if os.path.exists(specs_path) else {}
changed = []
for model, x in idx.items():
    text = open(D + x['file']).read(); h = hashlib.sha256(text.encode()).hexdigest()
    rid = sql("select id from raw_docs where content_sha256=%s limit 1;" % lit(h))
    if not rid:
        rid = sql("insert into raw_docs(source,source_path,vendor,doc_type,title,content,content_sha256,processed,project) values "
                  "('milesight.com',%s,'Milesight','документація вендора',%s,%s,%s,false,'IoT') returning id;" % (lit(x['url']), lit(x['title']), lit(text), lit(h))).splitlines()[0]
        print('added', model, rid)
    rid = int(rid)
    if mp.get(model) != [rid]:
        mp[model] = [rid]; specs.pop(model, None); changed.append(model)
json.dump(mp, open(C + 'ds_map.json', 'w'), ensure_ascii=False, indent=0)
json.dump(specs, open(specs_path, 'w'), ensure_ascii=False, indent=1)
print('to extract:', changed)
if changed:
    subprocess.run([sys.executable, os.path.join(ROOT, 'build/specs.py')], check=True)
