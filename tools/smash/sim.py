import asyncio, sys, os, json
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath(sys.argv[1]); ST=sys.argv[2]; N=int(sys.argv[3]) if len(sys.argv)>3 else 3
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for run in range(N):
      ctx=await b.new_context(viewport={'width':852,'height':393})
      await ctx.add_init_script("try{localStorage.setItem('tantan-lang','ja');localStorage.setItem('tantan-save',JSON.stringify({pname:'ぽんぽこ',nmAsked:1,unlock:2}));localStorage.setItem('kenka-hints2','[]')}catch(e){}")
      pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
      await pg.goto(URL); await pg.wait_for_timeout(1500)
      await pg.evaluate(f"()=>{{openMenu(); mDo('{ST}')}}"); await pg.wait_for_timeout(1500)
      await pg.evaluate("()=>{window.__L={}; const L0=launch; launch=(o,d,k)=>{L0(o,d,k); const r=window.__L[o.name]||(window.__L[o.name]={n:0,maxvx:0,minx:1e9,maxx:0}); r.n++; r.maxvx=Math.max(r.maxvx,Math.abs(o.vx)); r.pct=o.pct};}")
      r=await pg.evaluate("""()=>{const g=window.__game; let i=0, log=[], playT=0, mx=0;
        for(;i<12000&&g.phase!=='tally';i++){ g.tick&&g.tick(); if(g.phase==='play'){playT++; for(const f of g.fighters){const r=window.__L[f.name]; if(r&&f.fly){r.minx=Math.min(r.minx,f.x|0);r.maxx=Math.max(r.maxx,f.x|0);r.ring=[RING.a|0,RING.b|0]}} for(const f of g.fighters) mx=Math.max(mx,f.pct||0);}
          if(i%600===0) log.push(g.fighters.map(f=>(f.stock??'-')+'/'+(f.pct??'-')+(f.out?'X':'')+(f.gone>0?'g':'')).join(' '));}
        return {L:window.__L, phase:g.phase, playSec:(playT/60).toFixed(1), maxPct:mx, log, end:g.fighters.map(f=>({n:f.name,st:f.stock,p:f.pct,out:!!f.out,isP:!!f.isP}))}}""")
      print(json.dumps(r,ensure_ascii=False)); print('errs',errs[:3]); await ctx.close()
    await b.close()
asyncio.run(main())
