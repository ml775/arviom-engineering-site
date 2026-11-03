#!/usr/bin/env python3
"""Сторінка «Впровадження» (vprovadzhennia.html) з content/cases.json."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_solutions import chrome, e, ROOT

_IMC = {}
def img_info(src):
    # (ширина, «деталізація»): абстрактні фони з майже нульовою деталізацією не показуємо
    if src not in _IMC:
        try:
            from PIL import Image, ImageStat, ImageFilter
            im = Image.open(os.path.join(ROOT, src)); g = im.convert('L')
            _IMC[src] = (im.size[0], ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).mean[0])
        except Exception:
            _IMC[src] = (0, 0)
    return _IMC[src]

def usable(src):
    return bool(src) and img_info(src)[1] >= 3

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


LCSS = """<style>
.lh{position:relative;height:clamp(440px,40vw,560px);overflow:hidden;background:#24364b;color:#fff}
.lh>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.lh::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,20,35,.62) 0%,rgba(10,20,35,.25) 55%,rgba(10,20,35,.05) 100%)}
.lh .wrap{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:40px;align-items:center;height:100%;min-height:0}
.lh .chips{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}
.lh .chips span{position:relative;font-size:14px;color:#fff;border:1px solid rgba(255,255,255,.6);padding:5px 12px 5px 16px;background:rgba(10,20,35,.35)}
.lh .chips span::before{content:"";position:absolute;left:-1px;top:-1px;bottom:-1px;width:5px;background:var(--blue);transform:skewX(-14deg)}
.lh h1{font-weight:400;font-size:clamp(30px,3.6vw,48px);line-height:1.1;color:#fff;text-wrap:balance;text-shadow:0 2px 18px rgba(0,0,0,.25)}
.lh .eyebrow{color:#fff;opacity:.9}
.lh .btn{margin-top:26px}
.lh-side{min-width:0;justify-self:end;width:100%;max-width:680px}
.lh-cards{display:flex;gap:16px;overflow:hidden;scroll-behavior:smooth;scroll-snap-type:x mandatory}
.lh-cards a{flex:0 0 calc((100% - 32px)/3);scroll-snap-align:start;background:rgba(255,255,255,.16);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.3);border-radius:6px;padding:14px;color:#fff;display:flex;flex-direction:column}
.lh-cards b{display:block;font-weight:400;font-size:15px;line-height:1.3;min-height:3.9em}
.lh-cards small{display:flex;align-items:center;gap:6px;margin:8px 0 10px;font-size:13px;opacity:.95}
.lh-cards small::before{content:"";width:5px;height:12px;background:#5aa0ff;transform:skewX(-14deg)}
.lh-cards img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:4px;margin-top:auto}
.lh-nav{display:flex;gap:8px;margin-top:16px;justify-content:flex-start}
.lh-nav button{width:36px;height:36px;border:0;border-radius:4px;background:var(--blue);color:#fff;font-size:20px;cursor:pointer}
.lh-nav button:focus-visible{outline:2px solid #fff;outline-offset:2px}
.lb{display:grid;grid-template-columns:280px minmax(0,1fr);gap:40px;align-items:start;padding-block:48px 80px}
.fl h2{font-weight:400;font-size:26px;margin-bottom:16px}
.fl details{background:var(--bg2);border-radius:8px;padding:6px 18px 14px;margin-bottom:14px}
.fl summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--line);font-size:17px;color:var(--ink)}
.fl summary i{font-style:normal;color:var(--muted)}
.fl .sub{padding-left:26px}
.fl .sub label{font-size:14px;color:var(--muted)}
.fl-promo{background:var(--soft);border-radius:8px;padding:22px 20px;margin-top:6px}
.fl-promo b{display:block;font-weight:500;font-size:18px;color:var(--ink)}
.fl-promo p{margin-top:8px;font-size:14px;color:var(--text)}
.fl-promo a{display:inline-block;margin-top:12px;color:var(--blue);font-size:15px}
.fl summary::-webkit-details-marker{display:none}
.fl summary::after{content:"";border:6px solid transparent;border-top-color:#8a96a6;margin-top:6px}
.fl details[open] summary::after{transform:rotate(180deg);margin-top:-6px}
.fl summary i{font-style:normal;color:var(--muted);font-size:14px;margin-left:6px}
.fl label{display:flex;gap:10px;align-items:center;padding:6px 0;font-size:15px;color:var(--text);cursor:pointer}
.fl label input{width:16px;height:16px;accent-color:var(--blue)}
.fl label em{display:none}
.fl .opts{padding-top:6px}
.fl .dev .opts{max-height:320px;overflow:auto}
.fl .rst{font:inherit;font-size:15px;background:none;border:0;color:var(--blue);cursor:pointer;padding:4px 0}
.lr .top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:18px;color:var(--muted);font-size:15px}
.lg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.lc{display:flex;flex-direction:column;background:var(--bg2);border-radius:8px;overflow:hidden;color:var(--ink);transition:box-shadow .3s,transform .3s}
.lc:hover{box-shadow:0 18px 50px rgba(20,40,80,.1);transform:translateY(-2px)}
.lc .im{position:relative;aspect-ratio:16/13;overflow:hidden;background:#dfe4ea}
.lc .im img{width:100%;height:100%;object-fit:cover;transition:transform .8s}
.lc:hover .im img{transform:scale(1.04)}
.lc .rb{position:absolute;left:0;top:14px;font-size:13px;color:#fff;background:rgba(10,20,35,.72);padding:4px 12px 4px 16px}
.lc .rb::before{content:"";position:absolute;left:-2px;top:0;bottom:0;width:6px;background:var(--blue);transform:skewX(-14deg)}
.lc .im.shot{background:var(--tile)}
.lc .im.shot img{object-fit:contain;padding:44px 16px 12px;filter:drop-shadow(0 8px 14px rgba(20,30,45,.12))}
.lc .tx{padding:16px 16px 18px;display:flex;flex-direction:column;gap:18px;flex:1}
.lc h3{font-weight:500;font-size:17px;line-height:1.3;text-wrap:balance}
.lc .mt{margin-top:auto;display:flex;gap:14px;align-items:center;font-size:14px;flex-wrap:wrap}
.lc .mt .pin{color:var(--muted);display:inline-flex;gap:6px;align-items:center}
.lc .mt .pin::before{content:"";width:8px;height:8px;border:1.5px solid var(--muted);border-radius:50% 50% 50% 0;transform:rotate(-45deg)}
.lc .mt .ind{color:var(--blue)}
.lc[hidden],.lc.pg{display:none!important}
.pgn{display:flex;justify-content:flex-end;align-items:center;gap:6px;margin-top:30px}
.pgn button{font:inherit;font-size:14px;min-width:30px;height:30px;border:0;border-radius:50%;background:none;color:var(--text);cursor:pointer;padding:0 6px}
.pgn button.on{background:var(--blue);color:#fff}
.pgn button:disabled{opacity:.35;cursor:default}
.pgn span{color:var(--muted);padding:0 4px}
.lr .none{padding:40px 0;color:var(--muted)}
.lr .note{margin-top:28px;font-size:14px;color:var(--muted)}
.fl-t{display:none}
@media (max-width:1100px){.lg{grid-template-columns:repeat(2,minmax(0,1fr))}.lh .wrap{grid-template-columns:1fr}.lh-side{display:none}}
@media (max-width:900px){.lb{grid-template-columns:1fr;gap:20px}.fl-t{display:block;font:inherit;background:var(--bg2);border:0;border-radius:6px;padding:10px 16px;color:var(--ink);cursor:pointer}.fl .grp{display:none}.fl.open .grp{display:block}.fl h2{display:none}}
@media (max-width:560px){.lg{grid-template-columns:1fr}.lr .top span+span{display:none}}
</style>"""

LJS = """<script>
(function(){
var cards=[].slice.call(document.querySelectorAll('.lc')),boxes=[].slice.call(document.querySelectorAll('.fl input')),PAGE=12,page=1;
var pgn=document.querySelector('.pgn'),cnt=document.querySelector('.lr .cnt'),none=document.querySelector('.lr .none'),grid=document.querySelector('.lg');
function sel(g){return boxes.filter(function(b){return b.name===g&&b.checked}).map(function(b){return b.value})}
function apply(){var G=['dir','obj','dev','src'],S={};G.forEach(function(g){S[g]=sel(g)});var n=0;
cards.forEach(function(c){var ok=G.every(function(g){if(!S[g].length)return true;var v=(c.dataset[g]||'').split(' ');return S[g].some(function(x){return v.indexOf(x)>-1})});
c.hidden=!ok;c.classList.remove('pg');if(ok){n++;if(n<=(page-1)*PAGE||n>page*PAGE)c.classList.add('pg')}});
cnt.textContent=n;none.hidden=n>0;
[].forEach.call(document.querySelectorAll('.fl details'),function(d){var k=d.querySelectorAll('input:checked').length,i=d.querySelector('summary i');if(i)i.textContent='('+k+')'});
var P=Math.ceil(n/PAGE),h='';if(P>1){h+='<button type="button" data-p="'+(page-1)+'"'+(page<=1?' disabled':'')+' aria-label="Назад">‹</button>';
var gap=false;for(var i=1;i<=P;i++){if(P>7&&i>2&&i<P-1&&Math.abs(i-page)>1){if(!gap)h+='<span>…</span>';gap=true;continue}gap=false;h+='<button type="button" data-p="'+i+'"'+(i===page?' class="on"':'')+'>'+i+'</button>'}
h+='<button type="button" data-p="'+(page+1)+'"'+(page>=P?' disabled':'')+' aria-label="Далі">›</button>'}pgn.innerHTML=h}
pgn.addEventListener('click',function(ev){var b=ev.target.closest('button');if(!b||b.disabled)return;page=+b.dataset.p;apply();grid.scrollIntoView({behavior:'smooth',block:'start'})});
boxes.forEach(function(b){b.addEventListener('change',function(){page=1;apply()})});
document.querySelector('.fl .rst').addEventListener('click',function(){boxes.forEach(function(b){b.checked=false});page=1;apply()});
var t=document.querySelector('.fl-t');t.addEventListener('click',function(){var f=document.querySelector('.fl');f.classList.toggle('open');t.setAttribute('aria-expanded',f.classList.contains('open'))});
var h=location.hash.slice(1),hb=boxes.filter(function(b){return b.name==='dir'&&b.value===h})[0];if(hb)hb.checked=true;
apply();
var tr=document.querySelector('.lh-cards');[].forEach.call(document.querySelectorAll('.lh-nav button'),function(b){b.addEventListener('click',function(){tr.scrollBy({left:(b.dataset.d==='1'?1:-1)*(tr.firstElementChild.offsetWidth+16)})})});
})();
</script>"""


def devs(c):
    out = []
    for x in (c.get('devices') or '').replace('(', ',').replace(')', ',').replace('—', ',').split(','):
        for w in x.split():
            w = w.strip()
            if re.match(r'^[A-Z]{2,3}\d', w):
                out.append(w)
    return out


def slug(x):
    return re.sub(r'[^0-9a-zа-яіїєґ]+', '-', x.lower()).strip('-')


def build():
    items = [dict(c, src='ua') for c in C['own']] + [dict(c, src='ms') for c in C['ms']]
    for c in items:
        if c.get('page'):
            c['link'] = c['page']['slug'] + '.html'
        if c.get('page') and not usable(c['image']):
            c['image'] = c['page']['hero']  # абстрактний фон без змісту → головне фото кейсу
        c['_dev'] = devs(c)
    feat = sorted([c for c in items if c.get('featured')], key=lambda c: c['featured'])
    hero = next((c for c in feat if c.get('page')), feat[0])
    hero_img = hero['page']['hero'] if hero.get('page') else hero['image']
    ext = lambda c: '' if not c['link'].startswith('http') else ' target="_blank" rel="noopener"'
    nb = lambda t: re.sub(r'(\d) (\d)', '\\1\u00a0\\2', t)
    side = ''.join(f'<a href="{e(c["link"])}"{ext(c)}><b>{e(nb(c["title"]))}</b><small>{e(DIRS[c["dir"]])} · {e(c["country"])}</small><img src="{e(c["image"])}" alt="" loading="lazy"></a>' for c in feat if c is not hero and "shot-" not in c["image"])
    # filters
    def row(name, v, lbl):
        return f'<label><input type="checkbox" name="{name}" value="{e(v)}">{e(lbl)}</label>'
    def grp(name, title, opts, open_=True, rows=None):
        rows = rows if rows is not None else ''.join(row(name, v, lbl) for v, lbl, n in opts)
        return f'<details class="grp {name}"{" open" if open_ else ""}><summary>{e(title)} <i>(0)</i></summary><div class="opts">{rows}</div></details>'
    cnt = lambda key, val: sum(1 for c in items if val in (c[key] if isinstance(c[key], list) else [c[key]]))
    g_dir = [(k, v, cnt('dir', k)) for k, v in C['directions'] if cnt('dir', k)]
    objs = sorted({c['obj'] for c in items})
    g_obj = [(slug(o), o, cnt('obj', o)) for o in objs]
    alld = sorted({d for c in items for d in c['_dev']})
    g_dev = [(d.lower(), d, sum(1 for c in items if d in c['_dev'])) for d in alld]
    g_src = [('ua', 'Україна', cnt('src', 'ua')), ('ms', 'Milesight у світі', cnt('src', 'ms'))]
    # напрям → вкладені типи об'єктів (як Industry → підтипи на milesight.com)
    nested = ''.join(row('dir', k, v) + '<div class="sub">' + ''.join(row('obj', slug(o), o) for o in sorted({c['obj'] for c in items if c['dir'] == k})) + '</div>' for k, v, n in g_dir)
    filters = grp('dir', 'Напрям', [], rows=nested) + grp('src', 'Де', g_src) + grp('dev', 'Обладнання', g_dev, False)
    promo = '<div class="fl-promo grp"><b>Ваш об\'єкт тут</b><p>Зробили впровадження на Milesight? Розкажіть — опублікуємо кейс із вашим логотипом.</p><a href="./#contact">Надіслати кейс →</a></div>'
    def lcard(c):
        rb = '<span class="rb">Україна</span>' if c['src'] == 'ua' else ''
        return (f'<a class="lc" href="{e(c["link"])}"{ext(c)} data-dir="{e(c["dir"])}" data-obj="{e(slug(c["obj"]))}" data-src="{c["src"]}" data-dev="{e(" ".join(d.lower() for d in c["_dev"]))}">'
                f'<div class="im{" shot" if "shot-" in c["image"] else ""}"><img src="{e(c["image"])}" alt="" loading="lazy">{rb}</div>'
                f'<div class="tx"><h3>{e(nb(c["title"]))}</h3><div class="mt"><span class="pin">{e(c["country"])}</span><span class="ind">{e(c["obj"])}</span></div></div></a>')
    order = [c for c in items if c['src'] == 'ua'] + sorted([c for c in items if c['src'] == 'ms'], key=lambda c: (not c.get('featured'), c.get('featured', 99)))
    cards = ''.join(lcard(c) for c in order)
    body = f"""{CSS}{LCSS}
<div class="lh"><img src="{e(hero_img)}" alt=""><div class="wrap"><div><div class="chips"><span>{e(DIRS[hero['dir']])}</span><span>{e(hero['obj'])}</span><span>{e(hero['country'])}</span></div><h1>{e(nb(hero['title']))}</h1><a class="btn" href="{e(hero['link'])}"{ext(hero)}>Детальніше</a></div>
<div class="lh-side"><div class="lh-cards">{side}</div><div class="lh-nav"><button type="button" data-d="-1" aria-label="Назад">‹</button><button type="button" data-d="1" aria-label="Далі">›</button></div></div></div></div>
<main><div class="wrap lb">
<aside class="fl" aria-label="Фільтри"><h2>Фільтр</h2><button type="button" class="fl-t" aria-expanded="false">Фільтри</button>{filters}<button type="button" class="rst grp">Скинути фільтри</button>{promo}</aside>
<div class="lr"><div class="top"><span>Знайдено: <b class="cnt">{len(items)}</b></span><span>Проєкти в Україні — разом із партнерами-інтеграторами</span></div>
<div class="lg">{cards}</div><p class="none" hidden>За цими фільтрами нічого не знайдено. Спробуйте прибрати частину позначок.</p><nav class="pgn" aria-label="Сторінки"></nav>
<p class="note">Кейси Milesight — стислий виклад нашими словами за матеріалами milesight.com, фото — Milesight.</p></div>
</div>
<section class="blk" style="padding-block:0 72px"><div class="wrap"><div class="cta"><div><h2>Хочете такий результат на своєму об'єкті?</h2><p>Розкажіть про задачу — підберемо обладнання й партнера-інтегратора.</p></div><a class="btn w" href="./#contact">Обговорити проєкт</a></div></div></section>
</main>{LJS}"""
    html = chrome(body, C['title'], 'cases')
    html = html.replace('<a href="solutions.html" aria-current="page">Рішення</a>', '<a href="solutions.html">Рішення</a>')
    html = html.replace('<a href="vprovadzhennia.html">Впровадження</a>', '<a href="vprovadzhennia.html" aria-current="page">Впровадження</a>', 1)
    open(os.path.join(ROOT, 'vprovadzhennia.html'), 'w').write(html)
    print('cases: vprovadzhennia.html', len(items))


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


PCSS2 = '''<style>
.cp-sec h2.ctr{text-align:center;margin-bottom:44px}
.cp-tabs nav a.on{background:var(--blue);color:#fff}
.cp-bg{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);align-items:center}
.cp-bg .card{grid-column:1/2;grid-row:1;position:relative;z-index:1;background:#fff;border-radius:10px;box-shadow:0 18px 50px rgba(20,40,80,.12);padding:44px 48px;margin-right:-80px}
.cp-bg .card h2{margin-bottom:20px}
.cp-bg .card p{font-size:18px;color:var(--text)}
.cp-bg .card p+p{margin-top:14px}
.cp-bg>img{grid-column:2/3;grid-row:1;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px}
.cp-ch3{display:grid;grid-template-columns:repeat(var(--n,3),minmax(0,1fr));gap:24px}
.cp-ch3>div{background:#fff;border:1px solid #c9d6e8;border-radius:10px;padding:32px 30px}
.cp-ch3 .ic{display:flex;align-items:center;justify-content:center;width:60px;height:60px;border-radius:50%;margin:0 auto 22px}
.cp-ch3 .ic svg{width:30px;height:30px}
.cp-ch3 .ic-nature{background:var(--blue)}.cp-ch3 .ic-tools{background:#8a96a6}.cp-ch3 .ic-system{background:#0a3f9a}
.cp-ch3 h3{font-weight:500;font-size:20px;margin-bottom:14px}
.cp-ch3 ul{list-style:none;display:grid;gap:10px}
.cp-ch3 li{padding-left:16px;position:relative;color:var(--text);font-size:16px}
.cp-ch3 li::before{content:"";position:absolute;left:0;top:.62em;width:6px;height:6px;border-radius:50%;background:var(--blue)}
.cp-diag figcaption{margin-top:16px;font-size:14px;color:var(--muted)}
.cp-bento{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:20px;margin-top:20px}
.sp{border-radius:10px;padding:22px;display:flex;gap:22px;align-items:center}
.sp h3{font-weight:500;font-size:20px;margin-bottom:8px}
.sp p{color:var(--text);font-size:16px;line-height:1.6}
.sp .ph{display:flex;gap:12px;flex:none}
.sp .ph img{width:172px;height:200px;object-fit:contain;background:#fff;padding:6px;border-radius:6px}
.sp-wide{grid-column:1/-1}
.sp-wide .st{flex:1}
.sp-left{flex-direction:row-reverse}
.sp-left .st,.sp-right .st{flex:1}
.sp-tall{grid-column:2;grid-row:2/4;flex-direction:column;align-items:stretch}
.sp-tall .ph{flex:1;min-height:240px}
.sp-tall .ph img{flex:1;min-width:0;width:auto;height:100%}
.sp-right .ph.n2{flex-direction:column}.sp-right .ph.n2 img{width:180px;height:120px}
.sp,.sp-left,.sp-tall{flex-direction:column;align-items:stretch}
.sp .ph,.sp-tall .ph,.sp-right .ph.n2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));flex:none;min-height:0}
.sp .ph.n1{grid-template-columns:1fr}
.sp .ph img,.sp-tall .ph img,.sp-right .ph.n2 img{width:100%;height:auto;max-height:260px;object-fit:contain;background:#fff;padding:10px;border-radius:6px}
.sp-tall{grid-row:auto;grid-column:auto}
.t-blue{background:#e8f1fb}.t-mint{background:#e8f5ef}.t-sand{background:#fbf5e8}.t-grey{background:#f2f4f7}
.cp-resb{background:linear-gradient(120deg,#0a3f9a 0%,#0b5cd6 60%,#2b7cf2 100%);color:#fff}
.cp-resb h2{color:#fff}
.cp-res4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.cp-res4>div{border:1px solid rgba(255,255,255,.45);border-radius:10px;padding:28px 30px;background:rgba(255,255,255,.06)}
.cp-res4 h3{font-weight:500;font-size:20px;color:#fff;margin-bottom:10px}
.cp-res4 p{color:rgba(255,255,255,.92);font-size:16px}
.cp-scada{margin:36px auto 0;background:#fff;border-radius:10px;padding:14px}
.cp-scada img{display:block;width:100%;border-radius:6px}
.cp-scada figcaption{padding:12px 6px 4px;font-size:14px;color:var(--muted)}
.cp-note2{margin-top:18px;font-size:14px;color:rgba(255,255,255,.85)}
.cp-pt{display:grid;grid-template-columns:260px minmax(0,1fr);gap:40px;align-items:center;border:1px solid var(--line);border-radius:10px;padding:36px 40px;max-width:1000px;margin:0 auto}
.cp-pt .lg{font-weight:500;font-size:26px;letter-spacing:.04em;color:var(--ink);text-align:center;border-right:1px solid var(--line);padding-right:30px}
.cp-pt p{font-size:17px;color:var(--text)}
@media (max-width:1000px){.cp-ch3{grid-template-columns:1fr}.cp-bento{grid-template-columns:1fr}.sp-tall{grid-column:auto;grid-row:auto}.cp-bg{grid-template-columns:1fr}.cp-bg .card{margin:-60px 16px 0;grid-row:2}.cp-bg>img{grid-column:1;grid-row:1}}
@media (max-width:640px){.sp{flex-direction:column!important;align-items:stretch}.sp .ph img{width:100%!important;height:200px!important}.sp .ph{flex-direction:column}.cp-res4{grid-template-columns:1fr}.cp-pt{grid-template-columns:1fr;padding:24px}.cp-pt .lg{border-right:0;padding-right:0}.cp-bg .card{padding:28px 24px}}
</style>'''

SPY = '''<script>
(function(){var a=[].slice.call(document.querySelectorAll('.cp-tabs nav a'));if(!('IntersectionObserver' in window))return;
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting)a.forEach(function(l){l.classList.toggle('on',l.getAttribute('href')==='#'+x.target.id)})})},{rootMargin:'-40% 0px -55% 0px'});
a.forEach(function(l){var t=document.querySelector(l.getAttribute('href'));if(t)io.observe(t)})})();
</script>'''


ICONS = {
 'nature': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l-5 7h3l-4 6h5v5h2v-5h5l-4-6h3z" fill="#fff"/></svg>',
 'tools': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 7.5a5 5 0 0 1-6.6 4.7L6.7 19.9a2 2 0 1 1-2.8-2.8l7.7-7.7A5 5 0 0 1 17.3 3l-3 3 .9 2.8 2.8.9z" fill="#fff"/></svg>',
 'system': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19.4 13a7.5 7.5 0 0 0 0-2l2-1.6-2-3.4-2.4 1a7 7 0 0 0-1.7-1L15 3.5h-4l-.4 2.5a7 7 0 0 0-1.7 1l-2.4-1-2 3.4L6.6 11a7.5 7.5 0 0 0 0 2l-2 1.6 2 3.4 2.4-1a7 7 0 0 0 1.7 1l.4 2.5h4l.4-2.5a7 7 0 0 0 1.7-1l2.4 1 2-3.4zM12 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z" fill="#fff"/></svg>'}


def case_page(c):
    P = c['page']
    def fv(a, b):
        nb = lambda x: e(x).replace('-', chr(0x2011)).replace(' × ', chr(0xa0) + '×' + chr(0xa0))
        if a == 'Обладнання':
            return '<ul class="eq">' + ''.join(f'<li>{nb(x)}</li>' for x in b.split(', ')) + '</ul>'
        return f'<b>{nb(b)}</b>'
    facts = ''.join(f'<div class="f f-{"eq" if a == "Обладнання" else "t"}"><span>{e(a)}</span>{fv(a, b)}</div>' for a, b in P['facts'] if b.strip() not in ('', '—', '-'))
    tabs = [('background', 'Передумови'), ('challenges', 'Виклики'), ('solution', 'Рішення'), ('results', 'Результат')] + ([('partner', 'Партнер')] if P.get('partner') else [])
    nav = ''.join(f'<a href="#{k}">{e(v)}</a>' for k, v in tabs)
    bg = P['background']
    ch = ''.join(f'<div class="rv"><i class="ic ic-{e(x["icon"])}">{ICONS.get(x["icon"], "")}</i><h3>{e(x["t"])}</h3><ul>{"".join(f"<li>{e(y)}</li>" for y in x["items"])}</ul></div>' for x in P['challenges'])
    def panel(x):
        ims = ''.join(f'<img src="{e(i)}" alt="" loading="lazy">' for i in x['imgs'])
        if not ims:
            return f'<div class="sp sp-{e(x["layout"])} t-{e(x["tint"])} rv"><div class="st"><h3>{e(x["t"])}</h3><p>{e(x["d"])}</p></div></div>'
        return f'<div class="sp sp-{e(x["layout"])} t-{e(x["tint"])} rv"><div class="st"><h3>{e(x["t"])}</h3><p>{e(x["d"])}</p></div><div class="ph n{len(x["imgs"])}">{ims}</div></div>'
    L = {1: ['wide'], 2: ['wide', 'wide'], 3: ['wide', 'left', 'right'], 4: ['wide', 'left', 'tall', 'right']}
    T = ['blue', 'mint', 'sand', 'grey']
    sols = P['solution'][:4]
    for k, x in enumerate(sols):
        x.setdefault('layout', L[len(sols)][k]); x.setdefault('tint', T[k % 4]); x['imgs'] = [i for i in (x.get('imgs') or []) if i != P.get('solution_img') and usable(i)][:2]
    sol = ''.join(panel(x) for x in sols)
    R = P['results']
    diag = f'<figure class="cp-diag"><img src="{e(P["solution_img"])}" alt="Схема рішення" loading="lazy"><figcaption>{e(P.get("solution_caption", ""))}</figcaption></figure>' if P.get('solution_img') else ''
    res = ''.join(f'<div class="rv"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in R['items'])
    place = dict(P['facts']).get('Локація', c['place'])
    SRC = f'<p class="cp-src">Джерело: Milesight. Стислий виклад нашими словами, фото — Milesight. <a href="{e(c['link'])}" target="_blank" rel="noopener">Повна історія на milesight.com ↗</a></p>'
    pname = dict(P['facts']).get('Партнер-інтегратор', '').split(' (')[0]
    PART = (f'<section id="partner" class="cp-sec"><div class="wrap"><h2 class="ctr">Партнер</h2><div class="cp-pt rv"><div class="lg">{e(pname)}</div><div><p>{e(P["partner"])}</p>{SRC}</div></div></div></section>'
            if P.get('partner') else f'<section class="cp-sec" style="padding-block:8px 0"><div class="wrap">{SRC}</div></section>')
    body = f"""{CSS}{PCSS}{PCSS2}
<div class="cp-hero"><img src="{e(P['hero'])}" alt=""><div class="wrap"><div class="eyebrow">Досвід Milesight у світі · {e(DIRS[c['dir']])}</div><h1>{e(P['h1'])}</h1><p>{e(P['sub'])}</p><span class="cp-loc">Локація: {e(place)}</span></div></div>
<div class="cp-facts"><div class="wrap"><div class="box">{facts}<a class="btn" href="{e(c['link'])}" target="_blank" rel="noopener">Оригінал кейсу</a></div></div></div>
<div class="cp-tabs"><div class="wrap"><nav aria-label="Розділи кейсу">{nav}</nav><div class="bc"><a href="./">Головна</a> › <a href="vprovadzhennia.html">Впровадження</a> › {e(DIRS[c['dir']])}</div></div></div>
<main>
<section id="background" class="cp-sec"><div class="wrap"><div class="cp-bg"><div class="card rv"><h2>Передумови</h2>{''.join(f'<p>{e(x)}</p>' for x in bg['text'])}</div><img src="{e(bg['img'] if usable(bg.get('img')) else P['hero'])}" alt="" loading="lazy"></div></div></section>
<section id="challenges" class="cp-sec" style="background:var(--bg2)"><div class="wrap"><h2 class="ctr">Виклики</h2><div class="cp-ch3" style="--n:{len(P['challenges'])}">{ch}</div></div></section>
<section id="solution" class="cp-sec"><div class="wrap"><h2 class="ctr">Рішення</h2>{diag}<div class="cp-bento">{sol}</div></div></section>
<section id="results" class="cp-sec cp-resb"><div class="wrap"><h2 class="ctr">Результат</h2><div class="cp-res4">{res}</div>{f'<figure class="cp-scada rv" style="max-width:{img_info(R["img"])[0] + 28}px"><img src="{e(R["img"])}" alt="" loading="lazy">' + (f'<figcaption>{e(R["caption"])}</figcaption>' if R.get('caption') else '') + '</figure>' if usable(R.get('img')) else ''}{f'<p class="cp-note2">{e(R["note"])}</p>' if R.get('note') else ''}</div></section>
{PART}
<section class="blk" style="padding-block:24px 72px"><div class="wrap"><div class="cta"><div><h2>Схожа задача на вашому об'єкті?</h2><p>Підберемо обладнання й знайдемо партнера-інтегратора у вашому регіоні.</p></div><a class="btn w" href="./#contact">Обговорити проєкт</a></div></div></section>
</main>{SPY}"""
    html = chrome(body, P['h1'], 'case')
    html = html.replace('<a href="solutions.html" aria-current="page">Рішення</a>', '<a href="solutions.html">Рішення</a>')
    html = html.replace('<a href="vprovadzhennia.html">Впровадження</a>', '<a href="vprovadzhennia.html" aria-current="page">Впровадження</a>', 1)
    open(os.path.join(ROOT, P['slug'] + '.html'), 'w').write(html)
    return P['slug'] + '.html'


if __name__ == '__main__':
    from gen_cases_v2 import case_page_v2  # сторінка кейсу — стиль milesight «non-invasive electricity» (варіант 2)
    pages = [case_page_v2(dict(c)) for c in C['own'] + C['ms'] if c.get('page')]
    print('case pages:', ', '.join(pages))
