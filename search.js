(function(){
var IC='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>';
var ICON={'Впровадження':'◎','Новина':'✦','Рішення':'▣','Серія':'≡','Сторінка':'→','Продукт':'▢'};
var ORDER={'Продукт':0,'Серія':1,'Рішення':2,'Впровадження':3,'Новина':4,'Сторінка':5};
var data=null,ov,inp,res,cur=-1,items=[];
function norm(s){return (s||'').toLowerCase().replace(/ё/g,'е').replace(/[’'ʼ`]/g,'')}
function sq(s){return norm(s).replace(/[^a-z0-9а-яіїєґ]+/g,'')}
function wd(s){return ' '+norm(s).replace(/[^a-z0-9а-яіїєґ]+/g,' ')}
function esc(s){return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function load(cb){if(data)return cb();fetch('search-index.json').then(function(r){return r.json()}).then(function(d){
  data=d.map(function(x){var ts=sq(x.t);return {o:x,t:wd(x.t),ts:ts,d:wd(x.d),x:wd(x.x),re:(x.k==='Продукт'&&ts.indexOf('x')>=0)?new RegExp('^'+ts.replace(/x/g,'[a-z0-9]')):null}});cb()}).catch(function(){res.innerHTML='<div class="sq-hint">Не вдалося завантажити пошук.</div>'})}
function find(q){
  var words=norm(q).split(/\s+/).filter(Boolean),qs=sq(q);if(!qs)return [];
  var out=[];
  data.forEach(function(r){
    var s=0;
    if(r.ts===qs)s+=100;else if(r.re&&r.re.test(qs))s+=90;else if(r.ts.indexOf(qs)===0)s+=60;else if(qs.length>2&&r.ts.indexOf(qs)>=0)s+=40;
    var all=true;
    words.forEach(function(w){
      var k=' '+w.replace(/[^a-z0-9а-яіїєґ]+/g,''),st=k.length>4?k.slice(0,k.length-(k.length>6?2:1)):k;
      if(k===' ')return;
      if(r.t.indexOf(k)>=0)s+=12;else if(r.d.indexOf(k)>=0)s+=5;else if(r.x.indexOf(k)>=0)s+=3;
      else if(r.t.indexOf(st)>=0)s+=/[0-9]/.test(k)?1:8;else if(r.d.indexOf(st)>=0||r.x.indexOf(st)>=0)s+=2;else all=false;
    });
    if(!all&&s<40)return;
    if(s>0)out.push([s-ORDER[r.o.k]*0.5,r.o]);
  });
  out.sort(function(a,b){return b[0]-a[0]});
  return out.slice(0,30).map(function(x){return x[1]});
}
function hint(){res.innerHTML='<div class="sq-hint">Наприклад: <i>UG65</i><i>термостат</i><i>лічильник води</i><i>готель</i></div>';
  [].forEach.call(res.querySelectorAll('i'),function(i){i.onclick=function(){inp.value=i.textContent;render()}})}
function render(){
  var q=inp.value.trim();cur=-1;
  if(!q){items=[];return hint()}
  items=find(q);
  if(!items.length){res.innerHTML='<div class="sq-hint">Нічого не знайдено за запитом «'+esc(q)+'». Спробуйте модель (WT101) або слово (датчик, шлюз).</div>';return}
  res.innerHTML=items.map(function(x){
    return '<a href="'+esc(x.u)+'"><div class="im">'+(x.i?'<img src="'+esc(x.i)+'" alt="" loading="lazy">':ICON[x.k]||'→')+'</div><div class="tx"><b>'+esc(x.t)+'</b><span>'+esc(x.d)+'</span></div><em>'+x.k+'</em></a>'}).join('');
  [].forEach.call(res.querySelectorAll('a'),function(a){a.onclick=function(){close();if(a.pathname===location.pathname&&a.hash){location.hash=a.hash}}});
  mark(0);
}
function mark(i){var a=res.querySelectorAll('a');if(!a.length)return;if(cur>=0&&a[cur])a[cur].classList.remove('cur');cur=(i+a.length)%a.length;a[cur].classList.add('cur');a[cur].scrollIntoView({block:'nearest'})}
function open(){build();ov.classList.add('on');inp.value='';res.innerHTML='';load(function(){render()});setTimeout(function(){inp.focus()},30)}
function close(){if(ov)ov.classList.remove('on')}
function build(){
  if(ov)return;
  ov=document.createElement('div');ov.className='sq-ov';
  ov.innerHTML='<div class="sq-box" role="dialog" aria-label="Пошук по сайту"><div class="sq-in">'+IC+'<input type="search" placeholder="Пошук: модель, датчик, кейс…" autocomplete="off" aria-label="Пошук"><kbd>Esc</kbd></div><div class="sq-res"></div></div>';
  document.body.appendChild(ov);
  inp=ov.querySelector('input');res=ov.querySelector('.sq-res');
  inp.addEventListener('input',function(){if(data)render()});
  ov.addEventListener('mousedown',function(e){if(e.target===ov)close()});
  ov.querySelector('kbd').onclick=close;
  inp.addEventListener('keydown',function(e){
    if(e.key==='ArrowDown'){e.preventDefault();mark(cur+1)}
    else if(e.key==='ArrowUp'){e.preventDefault();mark(cur-1)}
    else if(e.key==='Enter'){var a=res.querySelectorAll('a')[cur];if(a){e.preventDefault();a.click();if(!(a.pathname===location.pathname&&a.hash))location.href=a.href}}
  });
}
function init(){
  var h=document.querySelector('header .rt')||document.querySelector('header .hr');
  if(!h||document.querySelector('.sq-btn'))return;
  var b=document.createElement('button');b.type='button';b.className='sq-btn';b.title='Пошук по сайту ( / )';b.setAttribute('aria-label','Пошук по сайту');b.innerHTML=IC;
  b.onclick=open;h.insertBefore(b,h.firstChild);
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape')return close();
    var t=e.target,typing=t&&(/INPUT|TEXTAREA|SELECT/.test(t.tagName)||t.isContentEditable);
    if((e.key==='/'&&!typing)||((e.ctrlKey||e.metaKey)&&(e.key==='k'||e.key==='K'||e.key==='л'||e.key==='Л'))){e.preventDefault();open()}
  });
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
