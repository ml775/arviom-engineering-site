#!/usr/bin/env python3
"""Генерує learn.html (Навчання) з content/learn.json у стилі сторінки IoT Academy Milesight."""
import json, os, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
from gen_solutions import chrome
e = lambda s: html.escape(str(s), quote=True)
L = json.load(open(os.path.join(ROOT, 'content/learn.json')))
EXT = ' target="_blank" rel="noopener"'
P = json.load(open(os.path.join(ROOT, 'content/podcast.json')))
pod = ''.join(f'<a class="pe rv" href="https://youtu.be/{e(x["yt"])}"{EXT}><img src="img/podcast/ep{x["n"]}.webp" alt="" loading="lazy"><div><span>Випуск {x["n"]} · {e(x["dur"])}</span><b>{e(x["t"])}</b><small>{e(x["d"])}</small></div><em>Слухати ↗</em></a>' for x in P['episodes'])
aud = ''.join(f'<div class="rv"><i>0{i+1}</i><b>{e(a)}</b><span>{e(b)}</span></div>' for i, (a, b) in enumerate(L['audience']))
ours = ''.join(f'<div class="pc rv lc"><div class="ph"><img src="{e(im)}" alt="" loading="lazy"><div class="tx"><div class="tag">{e(f)}</div><h3>{e(t)}</h3></div></div><div class="in"><p>{e(d)}</p><a href="./#contact">Записатися →</a></div></div>' for t, d, f, im in L['ours'])
def _crs(x):
    c, t, u, m = x[:4]; pod = x[4] if len(x) > 4 else ''
    meta = f'<small>{e(m)}</small>' if m else ''
    if pod: return f'<div class="crs rv"><span>{e(c)}</span><b>{e(t)}</b>{meta}<a class="pb" href="{e(pod)}">Є українською в подкасті →</a><a class="ac" href="{e(u)}"{EXT}>Академія Milesight ↗</a></div>'
    return f'<a class="crs rv" href="{e(u)}"{EXT}><span>{e(c)}</span><b>{e(t)}</b>{meta}<em>Академія Milesight ↗</em></a>'
courses = ''.join(_crs(x) for x in L['courses'])
faq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(L['faq']))
CSS = '''<style>
.lc{padding:0;overflow:hidden;display:flex;flex-direction:column}
.lc .ph{position:relative;height:230px;color:#fff}.lc .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.lc .ph::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,60,150,.92) 0%,rgba(11,92,214,.55) 42%,rgba(11,92,214,0) 78%)}
.lc .ph .tx{position:relative;z-index:1;padding:20px 22px;display:flex;flex-direction:column;gap:10px}
.lc .ph .tag{align-self:flex-start;background:#fff;color:var(--blue);font-size:12.5px;padding:4px 10px;border-radius:3px}
.lc .ph h3{color:#fff;font-size:23px;font-weight:500;line-height:1.25;padding:0}
.lc .in{padding:20px 22px 22px;display:flex;flex-direction:column;gap:14px;flex:1}.lc .in p{padding:0}.lc .in a{margin-top:auto}
.lv{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:44px}
.lv>div{background:#fff;border-radius:10px;overflow:hidden;border:1px solid var(--line)}.lv img{width:100%;height:220px;object-fit:cover}
.lv .tx{padding:24px 26px}.lv h3{font-size:24px;margin-bottom:8px}.lv p{color:var(--muted)}.lv .tx a{display:inline-block;margin-top:14px}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;margin-top:44px;counter-reset:s}
.steps div{border-top:1.5px solid var(--blue);padding-top:18px}.steps b{display:block;font-weight:400;font-size:19px;color:var(--ink);margin-bottom:6px}.steps span{color:var(--muted);font-size:16px}
.steps small{display:block;color:var(--blue);font-size:14px;margin-bottom:6px}
.facts{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}.facts span{background:var(--soft);color:var(--blue);border-radius:99px;padding:7px 16px;font-size:15px}
.crsg{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin-top:44px}
.crs{background:#fff;border:1px solid var(--line);border-radius:8px;padding:22px;display:flex;flex-direction:column;gap:8px;color:var(--ink);min-height:170px;transition:background .3s}
.crs:hover{background:var(--soft)}.crs span{font-size:13px;color:var(--blue)}.crs b{font-weight:400;font-size:19px;line-height:1.3}.crs small{font-size:14px;color:var(--muted)}.crs em{font-style:normal;font-size:14px;color:var(--muted);margin-top:auto}
.pod{max-width:1000px;margin:44px auto 0;border-top:1px solid var(--line)}
.pe{display:grid;grid-template-columns:200px 1fr auto;gap:28px;align-items:center;padding:20px 12px;border-bottom:1px solid var(--line);color:var(--ink);transition:background .3s}.pe:hover{background:var(--soft)}
.pe img{width:200px;aspect-ratio:16/9;object-fit:cover;border:1px solid var(--line);border-radius:6px;background:#fff}.pe div{display:flex;flex-direction:column;gap:6px}
.pe span{font-size:13px;color:var(--blue)}.pe b{font-weight:400;font-size:21px;line-height:1.3}.pe small{font-size:15px;color:var(--muted);line-height:1.45}.pe em{font-style:normal;font-size:15px;color:var(--blue);white-space:nowrap}
@media (max-width:760px){.pe{grid-template-columns:120px 1fr;gap:16px;align-items:start;padding:16px 0}.pe img{width:120px}.pe em{grid-column:2}.pe b{font-size:18px}}
.crs .pb{align-self:flex-start;background:var(--chip);color:var(--blue);font-size:14px;padding:6px 12px;border-radius:99px;margin-top:4px}.crs .pb:hover{background:var(--blue);color:#fff}.crs .ac{font-size:14px;color:var(--muted);margin-top:auto}
.faq{max-width:1000px;margin:40px auto 0;border-top:1px solid var(--line)}.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;cursor:pointer;padding:22px 40px 22px 0;position:relative;font-size:18px;color:var(--ink)}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:6px;top:18px;font-size:24px;color:var(--blue);font-weight:300}.faq details[open] summary::after{content:"×"}
.faq p{color:var(--muted);padding:0 40px 22px 0}
@media (max-width:900px){.lv{grid-template-columns:1fr}.steps{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.steps{grid-template-columns:1fr}}
</style>'''
body = CSS + f'''<div class="hero"><img src="img/learn/banner-academy.webp" alt=""><div class="tx wrap"><div class="eyebrow">Навчання</div><h1>Навчання IoT для інтеграторів та інженерів</h1><p>Від основ LoRaWAN до офіційної сертифікації Milesight — з нашою підтримкою українською.</p><a class="btn" href="./#contact">Записатися на навчання</a></div></div>
<div class="tabs"><div class="wrap"><nav aria-label="Розділи"><a href="#who" class="on">Для кого</a><a href="#ours">Курси ARVIOM</a><a href="#podcast">Подкаст</a><a href="#cert">Сертифікація</a><a href="#open">Відкриті курси</a><a href="#faq">Питання</a></nav>
<div class="bc"><a href="./">Головна</a> › Навчання</div></div></div>
<main>
<section id="who" class="blk"><div class="wrap"><h2 class="st center">Для кого це навчання</h2><div class="ben">{aud}</div></div></section>
<section id="ours" class="blk alt"><div class="wrap"><h2 class="st center">Наші курси й практикуми</h2><p class="center" style="color:var(--muted);margin-top:12px">Українською, на реальному обладнанні. Розклад — за запитом: залиште заявку, і ми запропонуємо дату.</p><div class="pgrid">{ours}</div><p class="center" style="color:var(--muted);font-size:13px;margin-top:18px">Фото: джерело Milesight</p></div></section>
<section id="podcast" class="blk"><div class="wrap"><div class="eyebrow center">Подкаст ARVIOM Engineering</div><h2 class="st center">{e(P['title'])}</h2><p class="center" style="color:var(--muted);margin-top:12px;max-width:72ch;margin-inline:auto">{e(P['lead'])}</p><div class="pod">{pod}</div><p class="center" style="margin-top:32px"><a class="btn" href="{e(P['playlist'])}"{EXT}>Увесь подкаст на YouTube</a></p><p class="center" style="color:var(--muted);font-size:14px;margin-top:14px">{e(P['source'])}</p></div></section>
<section id="cert" class="blk alt"><div class="wrap"><div class="eyebrow center">Академія Milesight</div><h2 class="st center">Офіційна сертифікація Milesight</h2>
<p class="center" style="color:var(--muted);margin-top:12px;max-width:80ch;margin-inline:auto">Програми сертифікації дають глибоку галузеву експертизу. Зараз доступна програма «Розумне керування HVAC»; нові напрями Milesight додає поступово.</p>
<div class="lv">
<div class="rv"><img src="img/learn/specialist.webp" alt=""><div class="tx"><h3>Milesight IoT Certified Specialist</h3><p>Продукти й застосування: ключові можливості пристроїв, логіка рішень і проєктування під сценарій. 3 курси.</p><a href="https://milesight-academy.learnworlds.com/program/specialist-certificate-program-milesight-smart-hvac-management-solution"{EXT}>Програма Specialist ↗</a></div></div>
<div class="rv"><img src="img/learn/expert.webp" alt=""><div class="tx"><h3>Milesight IoT Certified Expert</h3><p>Усе з рівня Specialist плюс монтаж і експлуатація: встановлення на об'єкті, налаштування пристроїв, інтеграція. 9 курсів.</p><a href="https://milesight-academy.learnworlds.com/program/expert-certificate-program-milesight-smart-hvac-management-solution"{EXT}>Програма Expert ↗</a></div></div>
</div>
<div class="steps">
<div class="rv"><small>Крок 1</small><b>Кабінет</b><span>Реєстрація на платформі Академії: прогрес відео й отримані бейджі.</span></div>
<div class="rv"><small>Крок 2</small><b>Навчання</b><span>Відеоуроки й слайди курсів для глибокого розбору.</span></div>
<div class="rv"><small>Крок 3</small><b>Іспит</b><span>Онлайн-тест, 3 спроби на кожну сертифікацію.</span></div>
<div class="rv"><small>Крок 4</small><b>Сертифікат</b><span>Електронний сертифікат одразу після іспиту, його можна додати в LinkedIn.</span></div>
</div>
<div class="facts"><span>Безкоштовно</span><span>Англійською, зі слайдами</span><span>Сертифікат на 1 рік</span><span>Досвідченим — одразу іспит</span></div>
<p style="margin-top:28px"><a class="btn" href="https://milesight-academy.learnworlds.com/home"{EXT}>Перейти в Академію Milesight</a></p>
</div></section>
<section id="open" class="blk"><div class="wrap"><h2 class="st center">Відкриті курси</h2><p class="center" style="color:var(--muted);margin-top:12px">Окремі курси з програм сертифікації — без іспиту, для конкретної теми.</p><div class="crsg">{courses}</div></div></section>
<section id="faq" class="blk alt"><div class="wrap"><h2 class="st center">Питання</h2><div class="faq">{faq}</div></div></section>
<section class="blk" style="padding-block:24px 72px"><div class="wrap"><div class="cta"><div><h2>Хочете навчити команду?</h2><p>Організуємо вебінар або практикум на стенді під ваші задачі.</p></div><a class="btn w" href="./#contact">Залишити заявку</a></div></div></section>
</main>'''
open(os.path.join(ROOT, 'learn.html'), 'w').write(chrome(body, 'Навчання', 'learn').replace('<a href="./#learn">Навчання</a>', '<a href="learn.html" aria-current="page">Навчання</a>'))
print('learn.html')
