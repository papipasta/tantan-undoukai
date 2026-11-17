()=>{
  const out=[], vw=innerWidth, vh=innerHeight;
  const vis=e=>{ const r=e.getBoundingClientRect(), cs=getComputedStyle(e); return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'&&e.offsetParent!==null; };
  const name=e=>(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className?'.'+e.className.split(' ').join('.'):'')+' 「'+(e.textContent||'').trim().slice(0,16)+'」';
  for(const e of document.body.querySelectorAll('*')){
    if(!vis(e)||e.tagName==='CANVAS') continue; const r=e.getBoundingClientRect();
    let p=e.parentElement, inScroll=false; while(p){ const o=getComputedStyle(p).overflowY; if((o==='auto'||o==='scroll')&&p.scrollHeight>p.clientHeight+1){inScroll=true;break;} p=p.parentElement; }
    if(!inScroll&&(r.right>vw+1||r.left<-1||r.bottom>vh+1||r.top<-1)) out.push('画面外 '+name(e));
    if(e.children.length===0&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible') out.push('切れ '+name(e));
    const pe=e.parentElement; if(pe&&getComputedStyle(pe).display.includes('flex')&&pe.tagName==='BUTTON'){ const pr=pe.getBoundingClientRect(); if(r.right>pr.right+1) out.push('親から はみ出し '+name(e)); }
  }
  for(const b of document.querySelectorAll('button')){ if(!vis(b)) continue; const sp=b.querySelector('span'); const t=[...b.childNodes].find(n=>n.nodeType===3&&n.textContent.trim()); if(!sp||!t||!vis(sp)) continue;
    const rg=document.createRange(); rg.selectNodeContents(t); const lr=rg.getBoundingClientRect(), sr=sp.getBoundingClientRect(); if(lr.right>sr.left-8&&sr.left>lr.left) out.push('重なり／近すぎ '+name(b)); }
  for(const b of document.querySelectorAll('.mrow .mi, .mseg .mi, .pgrid .mi')){ if(!vis(b)) continue; const cs=getComputedStyle(b), room=b.clientWidth-(parseFloat(cs.paddingLeft)||0)-(parseFloat(cs.paddingRight)||0)-4; let w=0; for(const n of b.childNodes){ const rg=document.createRange(); rg.selectNodeContents(n); w=Math.max(w,rg.getBoundingClientRect().width); } if(w>room) out.push('札から はみ出し '+name(b)); }
  return [...new Set(out)];
}