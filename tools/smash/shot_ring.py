# リングの 予告と ちぢんだ あとを 撮る
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
      await pg.evaluate("()=>{const g=window.__game; for(let i=0;i<400&&g.phase!=='play';i++) g.tick(); for(const f of g.fighters) f.stock=9; for(let i=0;i<4000 && g.phase==='play' && !(RING.warn>0 && RING.warn<120);i++) g.tick();}")
      print(await pg.evaluate('()=>[frame, RING.warn, RING.step]')); await pg.wait_for_timeout(200); await pg.screenshot(path=f'{OUT}/{sz}_warn.png')
      await pg.evaluate("()=>{const g=window.__game; for(let i=0;i<45*60 && g.phase==='play';i++) g.tick();}")
      await pg.wait_for_timeout(200); await pg.screenshot(path=f'{OUT}/{sz}_small.png')
      r=await pg.evaluate("()=>[RING.a|0,RING.b|0, window.__game.fighters.map(f=>f.x|0).join(',')]")
      print(sz, errs[:3], r); await ctx.close()
    await b.close()
asyncio.run(main())
