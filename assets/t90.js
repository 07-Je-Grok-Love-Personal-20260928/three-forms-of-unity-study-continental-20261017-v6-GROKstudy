/* t90：真实地图图片空闲预载（切换到「真实地图」时不再卡顿）；主题菜单键盘导航 */
(function(){var d=document;
var ric=window.requestIdleCallback||function(f){return setTimeout(f,200)};
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var im=e.target.querySelector('.mx-r img');if(!im)return;ric(function(){im.loading='eager';if(im.decode)im.decode().catch(function(){})},{timeout:3000})})},{rootMargin:'900px 0px'});
d.querySelectorAll('.mapx').forEach(function(x){io.observe(x)})}
var mm=d.getElementById('thmm');if(mm)mm.addEventListener('keydown',function(e){var bs=[].slice.call(mm.querySelectorAll('button')),i=bs.indexOf(d.activeElement);if(i<0)return;var k=e.key,n=null;if(k==='ArrowDown')n=i+2;else if(k==='ArrowUp')n=i-2;else if(k==='ArrowRight')n=i+1;else if(k==='ArrowLeft')n=i-1;if(n==null)return;e.preventDefault();bs[(n+bs.length)%bs.length].focus()});
})();
