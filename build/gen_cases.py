#!/usr/bin/env python3
"""Сторінка «Впровадження» (vprovadzhennia.html) з content/cases.json."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_solutions import chrome, e, ROOT

C = json.load(open(os.path.join(ROOT, 'content/cases.json')))
DIRS = dict(C['directions'])

CSS = '''<style>
.cs-hero{background:var(--tile);border-bottom:1px solid var(--line)}
.cs-hero .wrap{display:block;min-height:0;padding-block:72px 56px}
.cs-hero .eyebrow{color:var(--blue)}
.cs-hero h1{font-weight:300;font-size:clamp(32px,4vw,54px);line-height:1.08;max-width:22ch;color:var(--ink);text-wrap:balance}
.cs-hero p{margin-top:16px;max-width:60ch;color:var(--text);font-size:18px}
.cs-f{display:flex;gap:8px;flex-wrap:wrap;margin-top:28px}
.cs-f button{font:inherit;font-size:15px;border:1px solid var(--line);background:#fff;color:var(--text);border-radius:99px;padding:7px 16px;cursor:pointer}
.cs-f button[aria-pressed="true"]{background:var(--blue);border-color:var(--blue);color:#fff}
.cs-f button:focus-visible{outline:2px solid var(--blue);outline-offset:3px}
.cs-sec h2{font-weight:300;font-size:clamp(26px,2.6vw,34px);margin-bottom:24px}
.cs-sec h2 small{font-size:16px;color:var(--muted);margin-left:10px}
.cs-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.cs-c{position:relative;display:block;min-height:380px;border-radius:10px;overflow:hidden;color:#fff;background:#24364b}
.cs-c img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s ease}
.cs-c:hover img{transform:scale(1.05)}
.cs-c::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,20,35,.15) 0%,rgba(10,20,35,.2) 35%,rgba(10,20,35,.88) 100%)}
.cs-c .ov{position:absolute;inset:0;z-index:1;display:flex;flex-direction:column;justify-content:space-between;padding:22px}
.cs-c .ch{display:flex;gap:6px;flex-wrap:wrap}
.cs-c .ch span{font-size:13px;border-radius:3px;padding:2px 9px;background:#fff;color:var(--blue)}
.cs-c .ch span.own{background:var(--blue);color:#fff}
.cs-c h3{font-weight:400;font-size:22px;line-height:1.25;color:#fff;text-wrap:balance}
.cs-c .pl{margin-top:8px;font-size:14px;color:rgba(255,255,255,.85)}
.cs-c .more{display:grid;grid-template-rows:0fr;transition:grid-template-rows .4s ease}
.cs-c .more>div{overflow:hidden}
.cs-c:hover .more,.cs-c:focus-visible .more{grid-template-rows:1fr}
.cs-c p{margin-top:10px;font-size:15px;color:rgba(255,255,255,.92)}
.cs-c .dv{margin-top:6px;font-size:13px;color:rgba(255,255,255,.8)}
.cs-c .src{margin-top:12px;font-size:14px;color:#fff;opacity:.9}
.cs-c:focus-visible{outline:2px solid var(--blue);outline-offset:3px}
.cs-own .cs-c{min-height:440px}
.cs-own .cs-c::after{background:linear-gradient(90deg,rgba(10,20,35,.94) 0%,rgba(10,20,35,.82) 42%,rgba(10,20,35,.15) 100%)}
.cs-own .cs-c img{object-position:right top}
.cs-own .cs-c .ov{padding:36px 40px}
.cs-own .cs-c h3{font-weight:300;font-size:clamp(28px,3vw,40px);max-width:24ch}
.cs-own .cs-c .more{grid-template-rows:1fr}
.cs-own .cs-c p{max-width:60ch;font-size:17px}
@media (hover:none){.cs-c .more{grid-template-rows:1fr}}
.cs-empty{color:var(--muted);padding:24px 0}
[hidden]{display:none!important}
.cs-note{margin-top:28px;font-size:14px;color:var(--muted)}
@media (max-width:1000px){.cs-g{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.cs-g{grid-template-columns:1fr}.cs-c{min-height:340px}.cs-hero .wrap{padding-block:48px 40px}}
</style>'''

JS = '''<script>
(function(){var b=document.querySelectorAll('.cs-f button'),c=document.querySelectorAll('[data-dir]');
function set(d){b.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.f===d)});
c.forEach(function(x){x.hidden=!(d==='all'||x.dataset.dir===d)});
document.querySelectorAll('.cs-g').forEach(function(g){var e=g.parentNode.querySelector('.cs-empty');if(e)e.hidden=!!g.querySelector('[data-dir]:not([hidden])')})}
b.forEach(function(x){x.addEventListener('click',function(){set(x.dataset.f)})});
var h=location.hash.slice(1);set(document.querySelector('.cs-f [data-f="'+h+'"]')?h:'all')})();
</script>'''


def card(c, own):
    c = dict(c, title=re.sub(r'(\d) (\d)', '\\1\u00a0\\2', c['title']))
    ext = '' if not c['link'].startswith('http') else ' target="_blank" rel="noopener"'
    chips = (f'<span class="own">Проєкт ARVIOM</span>' if own else '') + f'<span>{e(DIRS[c["dir"]])}</span>'
    dv = f'<div class="dv">Обладнання: {e(c["devices"])}</div>' if c.get('devices') else ''
    src = '<div class="src">Детальніше →</div>' if own else '<div class="src">Джерело: Milesight ↗</div>'
    return (f'<a class="cs-c" data-dir="{e(c["dir"])}" href="{e(c["link"])}"{ext}><img src="{e(c["image"])}" alt="" loading="lazy">'
            f'<div class="ov"><div class="ch">{chips}</div><div><h3>{e(c["title"])}</h3><div class="pl">{e(c["place"])}</div>'
            f'<div class="more"><div><p>{e(c["text"])}</p>{dv}{src}</div></div></div></div></a>')


def build():
    btns = '<button type="button" data-f="all" aria-pressed="true">Усі</button>' + ''.join(
        f'<button type="button" data-f="{k}" aria-pressed="false">{e(v)}</button>' for k, v in C['directions'])
    body = f'''{CSS}
<div class="cs-hero"><div class="wrap"><div class="eyebrow">{e(C['title'])}</div><h1>{e(C['h1'])}</h1><p>{e(C['lead'])}</p>
<div class="cs-f" role="group" aria-label="Напрям">{btns}</div></div></div>
<main>
<section class="blk cs-sec cs-own"><div class="wrap"><h2>Проєкти ARVIOM</h2><div class="cs-g" style="grid-template-columns:1fr">{''.join(card(c, True) for c in C['own'])}</div>
<div class="cs-empty" hidden>У цьому напрямі наші проєкти готуються до публікації.</div></div></section>
<section class="blk alt cs-sec"><div class="wrap"><h2>Досвід Milesight у світі <small>{len(C['ms'])} кейсів</small></h2><div class="cs-g">{''.join(card(c, False) for c in C['ms'])}</div>
<div class="cs-empty" hidden>У цьому напрямі кейси ще додаються.</div>
<p class="cs-note">Стислий виклад нашими словами за матеріалами milesight.com. Повні історії — за посиланнями на картках.</p></div></section>
<section class="blk" style="padding-block:24px 72px"><div class="wrap"><div class="cta"><div><h2>Хочете такий результат на своєму об'єкті?</h2><p>Розкажіть про задачу — підберемо обладнання й покажемо схожі рішення.</p></div><a class="btn w" href="./#contact">Обговорити проєкт</a></div></div></section>
</main>{JS}'''
    html = chrome(body, C['title'], 'cases')
    # у шапці активний пункт — «Впровадження», а не «Рішення»
    html = html.replace('<a href="solutions.html" aria-current="page">Рішення</a>', '<a href="solutions.html">Рішення</a>')
    html = html.replace('<a href="vprovadzhennia.html">Впровадження</a>', '<a href="vprovadzhennia.html" aria-current="page">Впровадження</a>', 1)
    open(os.path.join(ROOT, 'vprovadzhennia.html'), 'w').write(html)
    print('cases: vprovadzhennia.html', len(C['ms']) + len(C['own']))


if __name__ == '__main__':
    build()
