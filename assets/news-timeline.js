(function(){
  var scroll=document.querySelector('.timeline-scroll');
  var nodes=Array.prototype.slice.call(document.querySelectorAll('.timeline-node'));
  var detail=document.getElementById('timeline-detail');
  if(!scroll||!nodes.length||!detail)return;
  var origin=nodes.find(function(node){return node.dataset.kind==='origin';})||nodes[0];
  var kind=document.getElementById('timeline-detail-kind');
  var issue=document.getElementById('timeline-detail-issue');
  var period=document.getElementById('timeline-detail-period');
  var title=document.getElementById('timeline-detail-title');
  var desc=document.getElementById('timeline-detail-desc');
  var link=document.getElementById('timeline-detail-link');
  var originButton=document.getElementById('timeline-origin');
  var labels={history:'历史月刊',origin:'网站上线原点',current:'上线后资讯'};
  var active=null;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function center(node,smooth){
    var left=node.offsetLeft-(scroll.clientWidth-node.offsetWidth)/2;
    scroll.scrollTo({left:Math.max(0,left),behavior:smooth&&!reduce?'smooth':'auto'});
  }
  function select(node,move){
    if(!node)return;
    nodes.forEach(function(item){
      var on=item===node;
      item.classList.toggle('is-active',on);
      item.setAttribute('aria-pressed',on?'true':'false');
    });
    active=node;
    kind.textContent=labels[node.dataset.kind]||'银发资讯';
    issue.textContent=node.dataset.issue;
    period.textContent=node.dataset.period;
    title.textContent=node.dataset.title;
    desc.textContent=node.dataset.desc;
    link.href=node.dataset.url;
    link.setAttribute('aria-label','阅读'+node.dataset.issue+'：'+node.dataset.title);
    detail.classList.remove('is-changing');
    void detail.offsetWidth;
    detail.classList.add('is-changing');
    if(move)center(node,true);
  }
  nodes.forEach(function(node,index){
    node.addEventListener('mouseenter',function(){select(node,false);});
    node.addEventListener('focus',function(){select(node,false);});
    node.addEventListener('click',function(){select(node,true);});
    node.addEventListener('keydown',function(event){
      if(event.key!=='ArrowLeft'&&event.key!=='ArrowRight')return;
      event.preventDefault();
      var next=index+(event.key==='ArrowRight'?1:-1);
      if(nodes[next]){nodes[next].focus();select(nodes[next],true);}
    });
  });
  if(originButton)originButton.addEventListener('click',function(){select(origin,true);origin.focus();});
  var dragging=false,startX=0,startLeft=0;
  scroll.addEventListener('pointerdown',function(event){
    if(event.pointerType==='mouse'){dragging=true;startX=event.clientX;startLeft=scroll.scrollLeft;scroll.setPointerCapture(event.pointerId);}
  });
  scroll.addEventListener('pointermove',function(event){
    if(dragging)scroll.scrollLeft=startLeft-(event.clientX-startX);
  });
  scroll.addEventListener('pointerup',function(){dragging=false;});
  scroll.addEventListener('pointercancel',function(){dragging=false;});
  select(origin,false);
  requestAnimationFrame(function(){center(origin,false);});
})();