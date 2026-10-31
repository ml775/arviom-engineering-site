import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from uk import UK,SERIES,IND,CMP
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP=ROOT+'/content/catalog/'
ser=json.load(open(SP+'sensor_series.json')); cat=json.load(open(SP+'iot_catalog.json'))
from PIL import Image
def img(n): return 'img/cat/cat-'+n.rsplit('.',1)[0]+'.webp'
def hh(path,T=135*135,HMAX=200,WMAX=230):
    w,h=Image.open(ROOT+'/'+path).size
    hd=(T*h/w)**.5
    hd=min(hd,HMAX,WMAX*h/w)
    return round(hd)
OURS={'EM300-TH':'em300-th','EM320-TH':'em320-th','EM300-DI':'em300-di','EM300-MCS':'em300-mcs','EM300-CL':'em300-cl','EM300-SLD/ZLD':'em300-sld','EM300-MLD':'em300-mld','EM320-TILT':'em320-tilt'}
SPECS=json.load(open(SP+'specs.json')) if os.path.exists(SP+'specs.json') else {}
FILES=json.load(open(SP+'series_files.json')) if os.path.exists(SP+'series_files.json') else {}
MFILE={}
for s in json.load(open(SP+'sensor_series.json')):
    if s['key'] in FILES:
        for p in s['products']: MFILE.setdefault(p['model'],FILES[s['key']])
for src,k in [('lorawan-gateway','gateways'),('lorawan-controller','controllers')]:
    for x in json.load(open(SP+'iot_catalog.json'))[src]['products']: MFILE.setdefault(x['title'][0],FILES.get(k,''))
def jslug(m): return re.sub(r'^-|-$','',re.sub(r'[^a-z0-9]+','-',m.lower()))
def link(model,href):
    if model in OURS: return 'catalog.html#m-'+OURS[model],0
    if model in SPECS and MFILE.get(model): return MFILE[model]+'#m-'+jslug(model),0
    return ('https://www.milesight.com'+href) if href.startswith('/') else href,1
def P(model,name,im,href):
    l,ext=link(model,href); i=img(im); return {'m':model,'n':UK.get(name,name),'i':i,'h':l,'x':ext,'s':hh(i)}
bykey={s['key']:s for s in ser}
products=[{'k':k,'t':SERIES[k],'f':FILES.get(k,''),'p':[P(p['model'],p['name'],p['img'],p['href']) for p in bykey[k]['products'] if p['model']!='Compatibility']} for k in SERIES]
industry=[{'t':t,'g':[{'k':k,'t':lab,'p':[P(p['model'],p['name'],p['img'],p['href']) for p in bykey[k]['products'] if p['model']!='Compatibility']} for k,lab in grp]} for t,grp in IND]
def simple(key): return [P(x['title'][0],' '.join(x['title'][1:]),x['img'].split('?')[0].split('/')[-1],x['href']) for x in cat[key]['products']]
gw=simple('lorawan-gateway'); ctl=simple('lorawan-controller'); disp=simple('iot-display')
cmp=[]
for x in cat['product-comparison']['products']:
    t=' '.join(x['title']); href=x['href']
    if 'temperature' in href or 'leakage' in href: href='catalog.html#compare'
    ci=img(x['img'].split('?')[0].split('/')[-1]); cmp.append({'t':CMP.get(t,t),'i':ci,'h':href,'x':0 if href.startswith('catalog') else 1,'s':hh(ci,T=200*75,HMAX=100,WMAX=260)})
data={'files':FILES,'series':products,'industry':industry,'gw':gw,'ctl':ctl,'disp':disp,'cmp':cmp}
tpl=open(ROOT+'/build/products_tpl.html').read()
open(ROOT+'/products.html','w').write(tpl.replace('__DATA__',json.dumps(data,ensure_ascii=False)))
print('series',len(products),'models',sum(len(s['p']) for s in products),'gw',len(gw),'ctl',len(ctl),'cmp',len(cmp))
miss=[p['n'] for s in products for p in s['p'] if re.search('[A-Za-z]{4,}',p['n']) and p['n']==p['n']]
print('untranslated:',[n for n in miss if not re.search('[а-яіїє]',n)])
