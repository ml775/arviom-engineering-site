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
    if c.get('page'): c['link'] = c['page']['slug'] + '.html'
    ext = '' if not c['link'].startswith('http') else ' target="_blank" rel="noopener"'
    chips = (f'<span class="own">Україна</span>' if own else '') + f'<span>{e(DIRS[c["dir"]])}</span>'
    dv = f'<div class="dv">Обладнання: {e(c["devices"])}</div>' if c.get('devices') else ''
    src = '<div class="src">Детальніше →</div>' if (own or c.get('page')) else '<div class="src">Джерело: Milesight ↗</div>'
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
<section class="blk cs-sec cs-own"><div class="wrap"><h2>Проєкти в Україні <small>разом із партнерами-інтеграторами</small></h2><div class="cs-g" style="grid-template-columns:1fr">{''.join(card(c, True) for c in C['own'])}</div>
<div class="cs-empty" hidden>У цьому напрямі проєкти в Україні готуються до публікації.</div></div></section>
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


PCSS = '''<style>
.cp-hero{position:relative;height:clamp(480px,46vw,640px);overflow:hidden;background:#24364b}
.cp-hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cp-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,20,35,.55) 0%,rgba(10,20,35,.15) 60%,rgba(10,20,35,0) 100%)}
.cp-hero .wrap{position:relative;z-index:1;display:block;min-height:0;padding-block:clamp(48px,6vw,88px) 0}
.cp-hero .eyebrow{color:#fff;opacity:.9}
.cp-hero h1{font-weight:400;font-size:clamp(32px,4.4vw,58px);line-height:1.08;color:#fff;max-width:22ch;text-wrap:balance;text-shadow:0 2px 20px rgba(0,0,0,.25)}
.cp-hero p{margin-top:16px;color:#fff;font-size:19px;max-width:48ch}
.cp-loc{display:inline-flex;align-items:center;gap:8px;margin-top:26px;background:#fff;color:var(--blue);border-radius:5px;padding:8px 16px;font-size:16px}
.cp-loc::before{content:"";width:9px;height:9px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--blue)}
.cp-facts{position:relative;z-index:2;margin-top:-92px}
.cp-facts .box{background:#fff;border-radius:10px;box-shadow:0 18px 50px rgba(20,40,80,.12);padding:28px 36px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.9fr) minmax(0,1.5fr) minmax(0,1fr) auto;gap:28px;align-items:center}
.cp-facts .f{border-right:1px solid var(--line);padding-right:24px;min-width:0}
.cp-facts .f span{display:block;font-size:14px;color:var(--muted)}
.cp-facts .f b{display:block;margin-top:6px;font-weight:400;font-size:17px;color:var(--ink)}
.cp-facts .f:nth-child(4){border-right:0}
.cp-facts .eq{list-style:none;margin-top:8px;display:flex;flex-wrap:wrap;gap:6px}
.cp-facts .eq li{font-size:15px;background:var(--bg2);border-radius:4px;padding:3px 9px;white-space:nowrap;color:var(--ink)}
.cp-diag{background:#fff;border:1px solid var(--line);border-radius:10px;padding:32px 36px;margin-bottom:28px}
.cp-diag img{display:block;width:100%;height:auto}
.cp-diag p{margin-top:16px;font-size:14px;color:var(--muted)}
.cp-tabs{position:sticky;top:64px;z-index:5;background:#fff;border-bottom:1px solid var(--line);margin-top:40px}
.cp-tabs .wrap{display:flex;justify-content:space-between;align-items:center;gap:20px;min-height:56px}
.cp-tabs nav{display:flex;gap:0;overflow-x:auto}
.cp-tabs nav a{padding:16px 22px;font-size:15px;letter-spacing:.04em;text-transform:uppercase;color:var(--text);border-right:1px solid var(--line);white-space:nowrap}
.cp-tabs nav a:last-child{border-right:0}
.cp-tabs nav a:hover{color:var(--blue)}
.cp-tabs .bc{font-size:14px;color:var(--muted);white-space:nowrap}
.cp-sec{padding-block:72px;scroll-margin-top:130px}
.cp-sec h2{font-weight:300;font-size:clamp(32px,3.6vw,48px);line-height:1.1;margin-bottom:28px}
.cp-two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:center}
.cp-two p{font-size:18px;color:var(--text)}
.cp-two p+p{margin-top:14px}
.cp-two img{width:100%;border-radius:10px}
.cp-ch{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.cp-ch div{background:#fff;border:1px solid var(--line);border-radius:10px;padding:28px}
.cp-ch h3{font-weight:500;font-size:20px;margin-bottom:12px}
.cp-ch ul{list-style:none;display:grid;gap:10px}
.cp-ch li{padding-left:18px;position:relative;color:var(--text)}
.cp-ch li::before{content:"";position:absolute;left:0;top:.65em;width:7px;height:7px;border-radius:50%;background:var(--blue)}
.cp-sol{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.cp-sol div{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.cp-sol .im{background:var(--tile);height:200px;display:flex;align-items:center;justify-content:center}
.cp-sol .im img{max-height:170px;max-width:85%;object-fit:contain}
.cp-sol h3{font-weight:500;font-size:19px;padding:20px 22px 0}
.cp-sol p{padding:10px 22px 24px;color:var(--muted);font-size:16px}
.cp-res{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.cp-res div{border-top:2px solid var(--blue);padding-top:14px}
.cp-res b{display:block;font-weight:500;font-size:18px}
.cp-res span{display:block;margin-top:6px;color:var(--muted)}
.cp-note{margin-top:22px;font-size:14px;color:var(--muted)}
.cp-src{font-size:14px;color:var(--muted);margin-top:18px}
.cp-src a{color:var(--blue)}
@media (max-width:1000px){.cp-facts .box{grid-template-columns:1fr 1fr;padding:22px}.cp-facts .f{border-right:0;padding-right:0}.cp-facts .btn{grid-column:1/-1;justify-self:start}.cp-sol{grid-template-columns:1fr 1fr}.cp-tabs .bc{display:none}}
@media (max-width:640px){.cp-two,.cp-ch,.cp-res,.cp-sol{grid-template-columns:1fr}.cp-facts .box{grid-template-columns:1fr}.cp-facts{margin-top:-60px}.cp-sec{padding-block:48px}.cp-tabs{top:64px}}
</style>'''


def case_page(c):
    P = c['page']
    def fv(a, b):
        nb = lambda x: e(x).replace('-', chr(0x2011)).replace(' × ', chr(0xa0) + '×' + chr(0xa0))
        if a == 'Обладнання':
            return '<ul class="eq">' + ''.join(f'<li>{nb(x)}</li>' for x in b.split(', ')) + '</ul>'
        return f'<b>{nb(b)}</b>'
    facts = ''.join(f'<div class="f f-{"eq" if a == "Обладнання" else "t"}"><span>{e(a)}</span>{fv(a, b)}</div>' for a, b in P['facts'])
    tabs = [('background', 'Передумови'), ('challenges', 'Виклики'), ('solution', 'Рішення'), ('results', 'Результат'), ('partner', 'Партнер')]
    nav = ''.join(f'<a href="#{k}">{e(v)}</a>' for k, v in tabs)
    bg = P['background']
    ch = ''.join(f'<div><h3>{e(t)}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>' for t, items in P['challenges'])
    sol = ''.join(f'<div><div class="im"><img src="{e(i)}" alt="" loading="lazy"></div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d, i in P['solution'])
    R = P['results']
    diag = f'<figure class="cp-diag"><img src="{e(P["solution_img"])}" alt="Схема рішення" loading="lazy"><p>{e(P.get("solution_caption", ""))}</p></figure>' if P.get('solution_img') else ''
    res = ''.join(f'<div><b>{e(t)}</b><span>{e(d)}</span></div>' for t, d in R['items'])
    place = dict(P['facts']).get('Локація', c['place'])
    body = f'''{CSS}{PCSS}
<div class="cp-hero"><img src="{e(P['hero'])}" alt=""><div class="wrap"><div class="eyebrow">Досвід Milesight у світі · {e(DIRS[c['dir']])}</div><h1>{e(P['h1'])}</h1><p>{e(P['sub'])}</p><span class="cp-loc">Локація: {e(place)}</span></div></div>
<div class="cp-facts"><div class="wrap"><div class="box">{facts}<a class="btn" href="{e(c['link'])}" target="_blank" rel="noopener">Оригінал кейсу</a></div></div></div>
<div class="cp-tabs"><div class="wrap"><nav aria-label="Розділи кейсу">{nav}</nav><div class="bc"><a href="./">Головна</a> › <a href="vprovadzhennia.html">Впровадження</a> › {e(DIRS[c['dir']])}</div></div></div>
<main>
<section id="background" class="cp-sec"><div class="wrap cp-two"><div><h2>Передумови</h2>{''.join(f'<p>{e(x)}</p>' for x in bg['text'])}</div><img src="{e(bg['img'])}" alt="" loading="lazy"></div></section>
<section id="challenges" class="cp-sec" style="background:var(--bg2)"><div class="wrap"><h2>Виклики</h2><div class="cp-ch">{ch}</div></div></section>
<section id="solution" class="cp-sec"><div class="wrap"><h2>Рішення</h2>{diag}<div class="cp-sol">{sol}</div></div></section>
<section id="results" class="cp-sec" style="background:var(--bg2)"><div class="wrap cp-two"><div><h2>Результат</h2><div class="cp-res">{res}</div>{f'<p class="cp-note">{e(R["note"])}</p>' if R.get('note') else ''}</div><img src="{e(R['img'])}" alt="" loading="lazy"></div></section>
<section id="partner" class="cp-sec"><div class="wrap"><h2>Партнер</h2><p style="font-size:18px;max-width:70ch;color:var(--text)">{e(P['partner'])}</p>
<p class="cp-src">Джерело: Milesight. Стислий виклад нашими словами, фото — Milesight. <a href="{e(c['link'])}" target="_blank" rel="noopener">Повна історія на milesight.com ↗</a></p></div></section>
<section class="blk" style="padding-block:24px 72px"><div class="wrap"><div class="cta"><div><h2>Схожа задача на вашому об'єкті?</h2><p>Підберемо обладнання й знайдемо партнера-інтегратора у вашому регіоні.</p></div><a class="btn w" href="./#contact">Обговорити проєкт</a></div></div></section>
</main>'''
    html = chrome(body, P['h1'], 'case')
    html = html.replace('<a href="solutions.html" aria-current="page">Рішення</a>', '<a href="solutions.html">Рішення</a>')
    html = html.replace('<a href="vprovadzhennia.html">Впровадження</a>', '<a href="vprovadzhennia.html" aria-current="page">Впровадження</a>', 1)
    open(os.path.join(ROOT, P['slug'] + '.html'), 'w').write(html)
    return P['slug'] + '.html'


if __name__ == '__main__':
    pages = [case_page(c) for c in C['own'] + C['ms'] if c.get('page')]
    print('case pages:', ', '.join(pages))
