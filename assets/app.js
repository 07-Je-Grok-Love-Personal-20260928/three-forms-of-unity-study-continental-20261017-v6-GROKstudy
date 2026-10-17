(function(){
var d=document,b=d.body,rm=matchMedia('(prefers-reduced-motion: reduce)').matches,$=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return [].slice.call((r||d).querySelectorAll(s))};
var T=window.TEC||{pages:[]},PG=b.dataset.page,KEY='tfu1.read',QK='tfu1.quiz';
function ld(k,def){try{var v=JSON.parse(localStorage.getItem(k));return v==null?def:v}catch(e){return def}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
/* reveal */
if(!rm&&'IntersectionObserver'in window){d.documentElement.classList.add('js');var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});$$('.reveal').forEach(function(el){io.observe(el)});setTimeout(function(){$$('.reveal').forEach(function(el){if(el.getBoundingClientRect().top<innerHeight)el.classList.add('in')})},50)}
/* toc */
var wide=function(){return innerWidth>=1100};
function tog(){if(wide())b.classList.toggle('tochide');else b.classList.toggle('tocopen')}
var tb=$('#tocbtn'),tx=$('#tocx');if(tb)tb.onclick=tog;if(tx)tx.onclick=tog;
$$('#toc a').forEach(function(a){a.addEventListener('click',function(){if(!wide())b.classList.remove('tocopen')})});
$$('.tg').forEach(function(t){t.onclick=function(){var li=t.closest('.t1');li.classList.toggle('closed');t.setAttribute('aria-expanded',!li.classList.contains('closed'))}});
$$('#toc .t1').forEach(function(li){if(!li.classList.contains('cur')){li.classList.add('closed');var g=$('.tg',li);if(g)g.setAttribute('aria-expanded','false')}});
var links={};$$('#toc .t1.cur a').forEach(function(a){var h=a.getAttribute('href');links[h.split('#')[1]]=a});
var secs=$$('section[id]'),cur=null;
var rd=ld(KEY,{}),mine=rd[PG]||[];
function markRead(id){if(mine.indexOf(id)<0){mine.push(id);rd[PG]=mine;sv(KEY,rd);var a=links[id];if(a)a.classList.add('done');upd()}}
function upd(){var c=$('#pgread');if(c)c.textContent=mine.length}
mine.forEach(function(id){var a=links[id];if(a)a.classList.add('done')});
var pend=$$('.reveal');function sweep(){if(!pend.length)return;pend=pend.filter(function(el){if(el.classList.contains('in'))return false;if(el.getBoundingClientRect().top<innerHeight){el.classList.add('in');return false}return true})}
function spy(){sweep();var y=innerHeight*0.25,act=null;for(var i=0;i<secs.length;i++){var r=secs[i].getBoundingClientRect();if(r.top<y)act=secs[i];if(secs[i].classList.contains('l2')&&r.top<innerHeight*0.6&&r.bottom>0)markRead(secs[i].id)}
var id=act&&act.id;if(act&&act.classList.contains('l1')){var f=$('.l2',act);if(f&&f.getBoundingClientRect().top<y)id=f.id}
if(id!==cur){$$('#toc a.on').forEach(function(a){a.classList.remove('on')});var a=links[id];if(a){a.classList.add('on');var l1=a.closest('.t1');if(l1){l1.classList.remove('closed')}if(wide()&&!b.classList.contains('tochide')){var t=$('#toc'),r2=a.getBoundingClientRect();if(r2.top<60||r2.bottom>innerHeight-40)t.scrollTop+=r2.top-innerHeight/2}}cur=id}
var h=d.documentElement,m=h.scrollHeight-innerHeight;var p=$('#prog');if(p)p.style.width=(m>0?h.scrollTop/m*100:0)+'%'}
var tk=0;addEventListener('scroll',function(){if(!tk){tk=1;requestAnimationFrame(function(){spy();tk=0})}},{passive:true});spy();upd();
/* counters */
var cs=$$('[data-count]');if(!rm&&cs.length){cs.forEach(function(c){var n=+c.dataset.count,t0=null;c.textContent='0';function st(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1400);c.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(st);else c.textContent=n}requestAnimationFrame(st);setTimeout(function(){c.textContent=n},2500)})}
/* tabs: scroll active into view */
var ta=$('.ptabs a.on');if(ta&&ta.parentNode)ta.parentNode.scrollLeft=Math.max(0,ta.offsetLeft-20);
/* exegesis open/close */
$$('[data-open]').forEach(function(x){x.onclick=function(){x.parentNode.previousElementSibling.querySelectorAll('details').forEach(function(e){e.open=true})}});
$$('[data-close]').forEach(function(x){x.onclick=function(){x.parentNode.previousElementSibling.querySelectorAll('details').forEach(function(e){e.open=false})}});
/* readers */
$$('[data-reader]').forEach(function(r){var zs=$$('.zh',r);
$$('[data-mode]',r).forEach(function(btn){btn.onclick=function(){var m=btn.dataset.mode;$$('[data-mode]',r).forEach(function(o){o.classList.toggle('ghost',o!==btn)});zs.forEach(function(z){z.classList.remove('masked','cue');if(m==='hide')z.classList.add('masked');if(m==='cue')z.classList.add('cue')})}});
$$('.verses li',r).forEach(function(li){li.onclick=function(){var z=$('.zh',li);if(z.classList.contains('masked')||z.classList.contains('cue'))z.classList.remove('masked','cue');else z.classList.add('masked')}})});
/* flip cards */
var fc=$('#fc'),seen={};$$('.flip').forEach(function(f,i){f.onclick=function(){f.classList.toggle('on');f.setAttribute('aria-pressed',f.classList.contains('on'));seen[i]=1;if(fc)fc.textContent=Object.keys(seen).length}});
/* quiz */
var qs=$('#qs');function score(){var n=$$('.opt.ok.picked').length;if(qs)qs.textContent=n;if(qs)sv(QK,{s:n,t:$$('.qq').length,d:$$('.qq').filter(function(q){return q.dataset.done}).length})}
$$('.qq').forEach(function(q){var a=+q.dataset.ans;$$('.opt',q).forEach(function(o){o.onclick=function(){if(q.dataset.done)return;q.dataset.done=1;var i=+o.dataset.i;o.classList.add('picked',i===a?'ok':'no');$$('.opt',q)[a].classList.add('ok');score()}})});
var qr=$('#qreset');if(qr)qr.onclick=function(){$$('.qq').forEach(function(q){delete q.dataset.done;$$('.opt',q).forEach(function(o){o.classList.remove('ok','no','picked')})});score()};
/* layers slider */
$$('[data-layers]').forEach(function(w){var r=$('input[type=range]',w),o=$('output',w),g=$('.lyrgrid',w),names=['只看第1层：使徒信经','叠到第2层：加上尼西亚新增','三层全开'];
function ap(){var v=+r.value;$$('.lyi',w).forEach(function(i){i.classList.toggle('off',+i.dataset.l>v)});if(o)o.textContent=names[v-1];w.dataset.v=v}
r.addEventListener('input',ap);ap()});
/* venn */
$$('.venn .vr').forEach(function(g){function go(){var t=d.getElementById('vreg-'+g.dataset.r);if(!t)return;t.scrollIntoView({behavior:rm?'auto':'smooth',block:'center'});$$('.vreg.hl').forEach(function(x){x.classList.remove('hl')});t.classList.add('hl');setTimeout(function(){t.classList.remove('hl')},2200)}
g.addEventListener('click',go);g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}})});
/* dort layers tabs */
$$('[data-dl]').forEach(function(w){var ps=$$('.dpan',w),ns=$$('.dnav a',w);if(!ps.length)return;w.classList.add('dl-js');function show(id){var ok=false;ps.forEach(function(p){var on=p.id===id;p.classList.toggle('on',on);if(on)ok=true});ns.forEach(function(a){a.classList.toggle('on',a.dataset.p===id)});return ok}
ns.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();show(a.dataset.p)})});
function hash(){var h=location.hash.slice(1);if(h&&d.getElementById(h)&&w.contains(d.getElementById(h))&&d.getElementById(h).classList.contains('dpan')){show(h);d.getElementById(h).scrollIntoView()}}
show(ps[0].id);hash();addEventListener('hashchange',hash)});
/* index progress */
var steps=$$('.step');if(steps.length){var tot=0,got=0;(T.pages||[]).forEach(function(p){var n=p.n,c=(rd[p.k]||[]).length;if(c>n)c=n;tot+=n;got+=c;var st=$('.step[data-pg="'+p.k+'"]');if(st){var i=$('.bar i',st),e=$('.pc',st);if(i)i.style.width=(n?c/n*100:0)+'%';if(e)e.textContent=c?(c>=n?'✓ 已读完':'已读 '+c+'/'+n):'未读';if(c>=n&&n)st.classList.add('done')}});
var pct=tot?Math.round(got/tot*100):0;var rf=$('#ringf'),rn=$('#ringn');if(rf)rf.setAttribute('stroke-dasharray',pct+' 100');if(rn)rn.textContent=pct+'%';var a=$('#readn'),z=$('#readt');if(a)a.textContent=got;if(z)z.textContent=tot;
var q=ld(QK,null),qe=$('#quizs');if(qe&&q)qe.textContent=q.s+' / '+q.t+(q.d<q.t?'（未答完）':'');
var rp=$('#resetp');if(rp)rp.onclick=function(){try{localStorage.removeItem(KEY);localStorage.removeItem(QK)}catch(e){}location.reload()}}
})();
