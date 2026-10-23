/* t89：地图图层切换、真实地图点按后缩放拖动（离开视口自动复位）、导航簇、锚点落点校正 */
(function(){var d=document,w=window;
function C(e,s){return e.target.closest?e.target.closest(s):null}
/* —— 锚点落点校正：content-visibility 占位高度与实际不符时，跳转后目标会被上方展开的区块推走 —— */
function land(){var id;try{id=decodeURIComponent(location.hash.slice(1))}catch(_){return}if(!id)return;var t=d.getElementById(id);if(!t)return;
 var n=0,stop=0;function u(){stop=1}w.addEventListener('wheel',u,{once:true,passive:true});w.addEventListener('touchstart',u,{once:true,passive:true});w.addEventListener('keydown',u,{once:true});
 (function f(){if(stop)return;var m=parseFloat(getComputedStyle(t).scrollMarginTop)||0,r=t.getBoundingClientRect().top-m;if(Math.abs(r)>3)w.scrollBy({top:r,behavior:'instant'});if(++n<16)setTimeout(f,n<5?60:160)})()}
w.addEventListener('hashchange',land);if(location.hash){if(d.readyState==='complete')land();else w.addEventListener('load',function(){setTimeout(land,30)})}
/* —— 真实地图 —— */
var act=null,io=null;
function S(x){return x._s||(x._s={k:1,tx:0,ty:0})}
function ap(x){var s=S(x),rm=x.querySelector('.rmv'),inn=x.querySelector('.rm-in'),vw=rm.clientWidth,vh=rm.clientHeight,cw=inn.offsetWidth*s.k,ch=inn.offsetHeight*s.k;
 s.tx=cw>vw?Math.min(0,Math.max(vw-cw,s.tx)):(vw-cw)/2;s.ty=ch>vh?Math.min(0,Math.max(vh-ch,s.ty)):(vh-ch)/2;inn.style.transform='translate('+s.tx+'px,'+s.ty+'px) scale('+s.k+')'}
function zm(x,f,px,py){var s=S(x),k=Math.min(8,Math.max(1,s.k*f));if(px==null){var rm=x.querySelector('.rmv');px=rm.clientWidth/2;py=rm.clientHeight/2}s.tx=px-(px-s.tx)*k/s.k;s.ty=py-(py-s.ty)*k/s.k;s.k=k;ap(x)}
function on(x){if(act&&act!==x)off(act);var rm=x.querySelector('.rmv'),s=S(x);s.k=1;s.tx=-rm.scrollLeft;s.ty=0;rm.scrollLeft=0;x.classList.add('rmon');act=x;ap(x);
 var P={},d0=0,k0=1,c0=null;
 x._h={down:function(e){if(C(e,'.rm-hs'))return;P[e.pointerId]=[e.clientX,e.clientY];rm.setPointerCapture&&rm.setPointerCapture(e.pointerId);var ks=Object.keys(P);if(ks.length===2){var a=P[ks[0]],b=P[ks[1]];d0=Math.hypot(a[0]-b[0],a[1]-b[1]);k0=S(x).k}},
  move:function(e){var p=P[e.pointerId];if(!p)return;var ks=Object.keys(P);if(ks.length===1){S(x).tx+=e.clientX-p[0];S(x).ty+=e.clientY-p[1];P[e.pointerId]=[e.clientX,e.clientY];ap(x)}else if(ks.length===2){P[e.pointerId]=[e.clientX,e.clientY];var a=P[ks[0]],b=P[ks[1]],dd=Math.hypot(a[0]-b[0],a[1]-b[1]),r=rm.getBoundingClientRect();if(d0)zm(x,k0*dd/d0/S(x).k,(a[0]+b[0])/2-r.left,(a[1]+b[1])/2-r.top)}e.preventDefault()},
  up:function(e){delete P[e.pointerId]},
  wheel:function(e){e.preventDefault();var r=rm.getBoundingClientRect();zm(x,Math.exp(-e.deltaY*.0015),e.clientX-r.left,e.clientY-r.top)},
  key:function(e){if(e.key==='Escape')off(x);else if(e.key==='+'||e.key==='=')zm(x,1.4);else if(e.key==='-')zm(x,1/1.4)}};
 rm.addEventListener('pointerdown',x._h.down);rm.addEventListener('pointermove',x._h.move);rm.addEventListener('pointerup',x._h.up);rm.addEventListener('pointercancel',x._h.up);rm.addEventListener('wheel',x._h.wheel,{passive:false});d.addEventListener('keydown',x._h.key);
 if('IntersectionObserver'in w){io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting&&act)off(act)})},{threshold:0});io.observe(x)}
 var b=x.querySelector('.rm-ctl button');b&&b.focus({preventScroll:true})}
function off(x){var rm=x.querySelector('.rmv'),inn=x.querySelector('.rm-in'),h=x._h;if(h){rm.removeEventListener('pointerdown',h.down);rm.removeEventListener('pointermove',h.move);rm.removeEventListener('pointerup',h.up);rm.removeEventListener('pointercancel',h.up);rm.removeEventListener('wheel',h.wheel);d.removeEventListener('keydown',h.key);x._h=null}
 if(io){io.disconnect();io=null}inn.style.transform='';x._s=null;x.classList.remove('rmon');if(act===x)act=null}
function tip(x,i){var li=x.closest('.rmap').querySelectorAll('.rm-leg li')[i],t=x.querySelector('.rm-tip');if(!li||!t)return;x.closest('.rmap').querySelectorAll('.rm-leg li.hit').forEach(function(l){l.classList.remove('hit')});li.classList.add('hit');t.innerHTML='<b>'+(+i+1)+'.</b> '+li.querySelector('.rmt').innerHTML;t.classList.add('show');clearTimeout(t._t);t._t=setTimeout(function(){t.classList.remove('show')},9000)}
d.addEventListener('click',function(e){var b;
 if(b=C(e,'.mx-tabs [data-l]')){var x=b.closest('.mapx');if(act&&x.contains(act))off(act);x.dataset.l=b.dataset.l;x.querySelectorAll('.mx-tabs [data-l]').forEach(function(y){y.setAttribute('aria-selected',y===b?'true':'false')});return}
 if(b=C(e,'.rm-go')){on(b.closest('.rmw'));return}
 if(b=C(e,'.rm-ctl [data-z]')){var x=b.closest('.rmw'),z=b.dataset.z;if(z==='x')off(x);else if(z==='0'){S(x).k=1;S(x).tx=0;S(x).ty=0;ap(x)}else zm(x,z==='1'?1.5:1/1.5);return}
 if(b=C(e,'.rm-hs')){tip(b.closest('.rmw'),b.dataset.i);return}
 if(b=C(e,'.rm-tip')){b.classList.remove('show');return}
 if(b=C(e,'.rm-leg li')){var f=b.closest('.rmap'),x=f.querySelector('.rmw');tip(x,b.dataset.i);var r=x.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)x.scrollIntoView({block:'nearest'});return}
 if(b=C(e,'#navc [data-nv]')){var v=b.dataset.nv;if(v==='back'){if(history.length>1)history.back();else location.href='index.html'}else if(v==='fwd')history.forward();else if(v==='top')w.scrollTo({top:0,behavior:'instant'});else if(v==='bot')w.scrollTo({top:d.documentElement.scrollHeight,behavior:'instant'});return}
 if(b=C(e,'#navc .nv-t')){var n=d.getElementById('navc'),o=!n.classList.contains('open');n.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');return}
 var n2=d.getElementById('navc');if(n2&&n2.classList.contains('open')&&!C(e,'#navc')){n2.classList.remove('open');n2.querySelector('.nv-t').setAttribute('aria-expanded','false')}});
d.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.matches&&e.target.matches('.rm-leg li')){e.target.click()}if(e.key==='Escape'){var n=d.getElementById('navc');if(n&&n.classList.contains('open')){n.classList.remove('open');n.querySelector('.nv-t').setAttribute('aria-expanded','false')}}});
w.addEventListener('resize',function(){if(act)ap(act)},{passive:true});
})();
;(function(){var L=document.querySelectorAll('.hx');if(!L.length)return;L.forEach(function(x){x.querySelectorAll('.hxl li').forEach(function(li,i){li.style.setProperty('--d',i)})});
if(!('IntersectionObserver'in window)){L.forEach(function(x){x.classList.add('hxon')});return}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('hxon');io.unobserve(e.target)}})},{rootMargin:'0px 0px -10% 0px'});L.forEach(function(x){io.observe(x)})})();
;(function(){var de=document.documentElement,t=document.querySelector('[data-mktog]'),b=document.querySelector('#navc [data-nv=mk]'),g=document.querySelector('#navc [data-nv=leg]'),L=document.querySelector('.mklegend');if(!t||!b)return;
b.hidden=false;if(L&&g){if(!L.id)L.id='mkleg';g.hidden=false;g.addEventListener('click',function(){L.scrollIntoView({block:'center'});L.classList.add('mkflash');setTimeout(function(){L.classList.remove('mkflash')},1600);var x=L.querySelector('[data-mktog]');x&&x.focus({preventScroll:true})})}
function p(){var on=!de.classList.contains('mkoff');b.setAttribute('aria-pressed',String(on));b.title='笔记标记：'+(on?'开（点按关闭）':'关（点按开启）')}
b.addEventListener('click',function(){var off=de.classList.toggle('mkoff');try{localStorage.setItem('mk.off',off?'1':'0')}catch(x){}document.querySelectorAll('[data-mktog]').forEach(function(x){x.setAttribute('aria-pressed',String(!off));x.textContent=off?'标记：关':'标记：开'});p()});document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('[data-mktog]'))setTimeout(p,0)});p()})();
