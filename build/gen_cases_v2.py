import re
#!/usr/bin/env python3
"""Сторінка кейсу у стилі milesight.com/success-stories/iot-non-invasive-electricity-monitoring… (прев'ю, варіант 2). Викликається з gen_cases.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_cases import C, CSS, DIRS, ICONS, SPY, chrome, e, usable, img_info, ROOT
from PIL import Image

V2CSS = '''<style>

.h2l{font-weight:300;font-size:clamp(30px,3.2vw,42px);line-height:1.1;margin-bottom:28px}
.v2-hero{position:relative;height:clamp(420px,38vw,520px);overflow:hidden;background:#24364b}
.v2-hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.v2-hero .wrap{position:relative;z-index:1;display:block;min-height:0;padding-block:0;height:100%}
.v2-hero .pan{position:absolute;left:var(--gutter,0);top:0;bottom:0;width:min(62%,780px);background:rgba(28,36,48,.78);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);border-radius:0 0 10px 10px;padding:clamp(36px,5vw,72px) clamp(28px,4vw,56px) 110px;display:flex;flex-direction:column;justify-content:center}
.v2-hero .eyebrow{color:#fff;opacity:.85}
.v2-hero h1{font-weight:400;font-size:clamp(28px,3.1vw,40px);line-height:1.18;color:#fff;text-wrap:balance}
.v2-hero p{margin-top:14px;color:rgba(255,255,255,.9);font-size:17px;max-width:52ch}
.v2-loc{display:inline-flex;align-items:center;gap:8px;margin-top:22px;background:var(--blue);color:#fff;border-radius:4px;padding:6px 12px;font-size:14px;align-self:flex-start}
.v2-loc::before{content:"";width:8px;height:8px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#fff}
.cp-facts{margin-top:-70px}
.cp-facts .box{border-radius:6px;padding:22px 30px}
.v2-bg{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);align-items:center}
.v2-bg .card{grid-column:1/2;grid-row:1;position:relative;z-index:1;background:#fff;border-radius:8px;box-shadow:0 18px 50px rgba(20,40,80,.12);padding:36px 40px;margin-right:-80px}
.v2-bg .card p{font-size:17px;color:var(--text)}.v2-bg .card p+p{margin-top:12px}
.v2-bg>img{grid-column:2/3;grid-row:1;width:100%;aspect-ratio:5/3;object-fit:cover;border-radius:8px}
.v2-ch{display:grid;grid-template-columns:repeat(var(--n,2),minmax(0,1fr));gap:24px}
.v2-ch>div{position:relative;background:#fff;border-radius:8px;box-shadow:0 10px 30px rgba(20,40,80,.06);padding:30px 60px 30px 30px}
.v2-ch .ic{position:absolute;right:-6px;top:-6px;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(20,40,80,.15)}
.v2-ch .ic svg{width:22px;height:22px}
.v2-ch .ic-nature{background:var(--blue)}.v2-ch .ic-tools{background:#1e9e6a}.v2-ch .ic-system{background:#0a3f9a}
.v2-ch h3{font-weight:500;font-size:19px;margin-bottom:10px}
.v2-ch p{color:var(--text);font-size:16px}
.v2-diag{max-width:1100px;margin:0 auto 36px}
.v2-diag img{display:block;width:100%;height:auto}
.v2-diag figcaption{margin-top:10px;font-size:13px;color:var(--muted);text-align:center}
.v2-prose p{font-size:17px;color:var(--text);max-width:1100px}
.v2-prose p+p{margin-top:12px}
.v2-prose b{font-weight:500;color:var(--ink)}
.v2-ph{display:grid;grid-template-columns:repeat(var(--n,4),minmax(0,1fr));gap:18px;margin-top:30px}
.v2-ph img{width:100%;height:280px;object-fit:cover;border-radius:6px}
.v2-sh{display:grid;grid-template-columns:repeat(var(--n,3),minmax(0,1fr));gap:18px;margin-top:22px}
.v2-sh img{width:100%;height:auto;max-height:300px;object-fit:contain;background:#fff;border:1px solid var(--line);border-radius:6px;padding:8px}
.v2-res{background:linear-gradient(160deg,#0a2650 0%,#0b3f8f 100%);color:#fff}
.v2-res h2{color:#fff;text-align:center}
.v2-res .g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.v2-res .g>div{border:1px solid rgba(255,255,255,.5);border-radius:8px;padding:26px 28px}
.v2-res .g>div:first-child{grid-column:1/-1}
.v2-res h3{font-weight:500;font-size:19px;color:#fff;margin-bottom:8px}
.v2-res p{color:rgba(255,255,255,.9);font-size:16px}
.v2-res figure{margin:36px auto 0;background:#fff;border-radius:8px;padding:12px}
.v2-res figure img{display:block;width:100%;border-radius:4px}
.v2-res figcaption{padding:10px 6px 2px;font-size:14px;color:var(--muted)}
.v2-res .note{margin-top:16px;font-size:14px;color:rgba(255,255,255,.8)}
.v2-pt{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);border-radius:8px;overflow:hidden;min-height:300px}
.v2-pt .l{background:#e9edf2;display:flex;align-items:center;justify-content:center;padding:40px}
.v2-pt .l span{background:#fff;border-radius:8px;padding:34px 42px;font-weight:500;font-size:26px;letter-spacing:.03em;color:var(--ink);text-align:center}
.v2-pt .r{background:#2c343d;color:#fff;padding:44px 48px}
.v2-pt .r h2{color:#fff;font-size:30px;font-weight:400;margin-bottom:16px}
.v2-pt .r p{color:rgba(255,255,255,.88);font-size:16px}
@media (max-width:1000px){.v2-hero .pan{width:auto;right:var(--gutter,0)}.v2-bg{grid-template-columns:1fr}.v2-bg .card{margin:-60px 16px 0;grid-row:2}.v2-bg>img{grid-column:1;grid-row:1}.v2-ch{grid-template-columns:1fr}.v2-ph{grid-template-columns:1fr 1fr}.v2-ph img{height:200px}.v2-sh{grid-template-columns:1fr}.v2-res .g{grid-template-columns:1fr}.v2-pt{grid-template-columns:1fr}}
</style>'''


def is_shot(src):
    """Скриншот інтерфейсу (світла площина) чи фото."""
    try:
        im = Image.open(os.path.join(ROOT, src)).convert('L').resize((64, 64))
        return sum(1 for p in im.getdata() if p > 225) / 4096 > .45
    except Exception:
        return False


def case_page_v2(c, out=None):
    P = c['page']
    nbx = lambda x: e(x).replace('-', chr(0x2011)).replace(' × ', chr(0xa0) + '×' + chr(0xa0))
    def fv(a, b):
        def li(x):
            m = re.match(r'(UR32[LS]?|UR35|UR41L?|UR75|UF31|UF51)\b', x.strip())
            if not m: return f'<li>{nbx(x)}</li>'
            return f'<li><a href="s-routers.html#m-{m.group(1).lower().rstrip("l") if m.group(1) == "UR41L" else m.group(1).lower()}">{nbx(x)}</a></li>'
        return '<ul class="eq">' + ''.join(li(x) for x in b.split(', ')) + '</ul>' if a == 'Обладнання' else f'<b>{nbx(b)}</b>'
    facts = ''.join(f'<div class="f f-{"eq" if a == "Обладнання" else "t"}"><span>{e(a)}</span>{fv(a, b)}</div>' for a, b in P['facts'] if b.strip() not in ('', '—', '-'))
    tabs = [('background', 'Передумови'), ('challenges', 'Виклики'), ('solution', 'Рішення'), ('results', 'Результат')] + ([('partner', 'Партнер')] if P.get('partner') else [])
    nav = ''.join(f'<a href="#{k}">{e(v)}</a>' for k, v in tabs)
    bg = P['background']
    ch = ''.join(f'<div class="rv"><i class="ic ic-{e(x["icon"])}">{ICONS.get(x["icon"], "")}</i><h3>{e(x["t"])}</h3><p>{e(" ".join(y.rstrip() + ("" if y.rstrip()[-1:] in ".!?" else ".") for y in x["items"]))}</p></div>' for x in P['challenges'])
    sols = P['solution'][:4]
    prose = ''.join(f'<p><b>{e(x["t"])}.</b> {e(x["d"])}</p>' for x in sols)
    imgs = [i for x in sols for i in (x.get('imgs') or []) if i != P.get('solution_img') and usable(i)]
    seen = []; [seen.append(i) for i in imgs if i not in seen]
    photos = [i for i in seen if not is_shot(i)][:4]; shots = [i for i in seen if is_shot(i)][:3]
    ph = f'<div class="v2-ph" style="--n:{len(photos)}">' + ''.join(f'<img src="{e(i)}" alt="" loading="lazy">' for i in photos) + '</div>' if photos else ''
    sh = f'<div class="v2-sh" style="--n:{len(shots)}">' + ''.join(f'<img src="{e(i)}" alt="" loading="lazy">' for i in shots) + '</div>' if shots else ''
    diag = f'<figure class="v2-diag"><img src="{e(P["solution_img"])}" alt="Схема рішення" loading="lazy"><figcaption>{e(P.get("solution_caption", ""))}</figcaption></figure>' if P.get('solution_img') else ''
    R = P['results']
    res = ''.join(f'<div class="rv"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in R['items'])
    rimg = (f'<figure class="rv" style="max-width:{img_info(R["img"])[0] + 24}px"><img src="{e(R["img"])}" alt="" loading="lazy">' + (f'<figcaption>{e(R["caption"])}</figcaption>' if R.get('caption') else '') + '</figure>') if usable(R.get('img')) else ''
    place = dict(P['facts']).get('Локація', c['place'])
    SRC = f'<p class="cp-src">Джерело: Milesight. Стислий виклад нашими словами, фото — Milesight. <a href="{e(c["link"])}" target="_blank" rel="noopener">Повна історія на milesight.com ↗</a></p>'
    pname = dict(P['facts']).get('Партнер-інтегратор', '').split(' (')[0]
    PART = (f'<section id="partner" class="cp-sec"><div class="wrap"><h2 class="h2l">Партнер</h2><div class="v2-pt rv"><div class="l"><span>{e(pname)}</span></div><div class="r"><h2>Про {e(pname)}</h2><p>{e(P["partner"])}</p></div></div>{SRC}</div></section>'
            if P.get('partner') else f'<section class="cp-sec" style="padding-block:8px 0"><div class="wrap">{SRC}</div></section>')
    from gen_cases import PCSS
    body = f"""{CSS}{PCSS}{V2CSS}
<div class="v2-hero"><img src="{e(P['hero'])}" alt=""><div class="wrap"><div class="pan"><div class="eyebrow">Досвід Milesight у світі · {e(DIRS[c['dir']])}</div><h1>{e(P['h1'])}</h1><p>{e(P['sub'])}</p><span class="v2-loc">{e(place)}</span></div></div></div>
<div class="cp-facts"><div class="wrap"><div class="box">{facts}<a class="btn" href="{e(c['link'])}" target="_blank" rel="noopener">Оригінал кейсу</a></div></div></div>
<div class="cp-tabs"><div class="wrap"><nav aria-label="Розділи кейсу">{nav}</nav><div class="bc"><a href="./">Головна</a> › <a href="vprovadzhennia.html">Впровадження</a> › {e(DIRS[c['dir']])}</div></div></div>
<main>
<section id="background" class="cp-sec"><div class="wrap"><h2 class="h2l">Передумови</h2><div class="v2-bg"><div class="card rv">{''.join(f'<p>{e(x)}</p>' for x in bg['text'])}</div><img src="{e(bg['img'] if usable(bg.get('img')) else P['hero'])}" alt="" loading="lazy"></div></div></section>
<section id="challenges" class="cp-sec" style="background:var(--bg2)"><div class="wrap"><h2 class="h2l">Виклики</h2><div class="v2-ch" style="--n:{min(len(P['challenges']), 3)}">{ch}</div></div></section>
<section id="solution" class="cp-sec"><div class="wrap"><h2 class="h2l" style="text-align:center">Рішення</h2>{diag}<div class="v2-prose">{prose}</div>{ph}{sh}</div></section>
<section id="results" class="cp-sec v2-res"><div class="wrap"><h2 class="h2l">Результат</h2><div class="g">{res}</div>{rimg}{f'<p class="note">{e(R["note"])}</p>' if R.get('note') else ''}</div></section>
{PART}
<section class="blk" style="padding-block:24px 72px"><div class="wrap"><div class="cta"><div><h2>Схожа задача на вашому об'єкті?</h2><p>Підберемо обладнання й знайдемо партнера-інтегратора у вашому регіоні.</p></div><a class="btn w" href="./#contact">Обговорити проєкт</a></div></div></section>
</main>{SPY}"""
    html = chrome(body, P['h1'], 'case')
    html = html.replace('<a href="solutions.html" aria-current="page">Рішення</a>', '<a href="solutions.html">Рішення</a>')
    html = html.replace('<a href="vprovadzhennia.html">Впровадження</a>', '<a href="vprovadzhennia.html" aria-current="page">Впровадження</a>', 1)
    out = out or P['slug'] + '.html'
    open(os.path.join(ROOT, out), 'w').write(html)
    return out


if __name__ == '__main__':
    key = sys.argv[1] if len(sys.argv) > 1 else 'dubai'
    c = next(x for x in C['own'] + C['ms'] if x.get('page') and key in x['page']['slug'])
    c = dict(c); c['link'] = c['link']
    print(case_page_v2(c, '_preview.html'))
