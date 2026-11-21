# きりふだ玉・カットイン・ちゃがま だいこうしん・GAME SET を撮る
import asyncio, sys, os
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath(sys.argv[1]); OUT=sys.argv[2]; LANG=sys.argv[3]; SIZES=sys.argv[4].split(',')
async def main():
  os.makedirs(OUT,exist_ok=True)
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for sz in SIZES:
      vw,vh=map(int,sz.split('x'))
      ctx=await b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,has_touch=vw<vh,is_mobile=vw<vh)
      await ctx.add_init_script(f"try{{localStorage.setItem('tantan-lang','{LANG}');localStorage.setItem('tantan-save',JSON.stringify({{pname:'ぽんぽこ',nmAsked:1,unlock:2}}));localStorage.setItem('kenka-hints2','[]')}}catch(e){{}}")
      pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
      await pg.goto(URL); await pg.wait_for_timeout(1500)
      await pg.evaluate("()=>{openMenu(); mDo('p10')}"); await pg.wait_for_timeout(1200)
      await pg.evaluate("()=>{const g=window.__game; for(let i=0;i<400&&g.phase!=='play';i++) g.tick(); for(let i=0;i<200;i++) g.tick(); kiriCD=1; for(let i=0;i<80;i++) g.tick(); const P=g.player; if(KIRI){KIRI.x=P.x+60; KIRI.tx=KIRI.x; KIRI.z=P.z; KIRI.tz=P.z;} }")
      await pg.wait_for_timeout(300); await pg.screenshot(path=f'{OUT}/{sz}_1orb.png')
      await pg.evaluate("()=>{const g=window.__game, P=g.player; KIRI=null; P.kiri=true; P.sp=SP_MAX; P.st='idle'; P.act=null; for(const f of g.fighters) if(f!==P){f.pct=80;} doSpecial(P);}")
      await pg.wait_for_timeout(450); await pg.screenshot(path=f'{OUT}/{sz}_2cut.png')
      await pg.wait_for_timeout(1300); await pg.screenshot(path=f'{OUT}/{sz}_3go.png')
      await pg.evaluate("()=>{GSET={t:0,k:'set'};}")
      await pg.wait_for_timeout(500); await pg.screenshot(path=f'{OUT}/{sz}_4set.png')
      m=await pg.evaluate("()=>[...trMiss].slice(-20)")
      print(sz, errs[:3], m); await ctx.close()
    await b.close()
asyncio.run(main())
