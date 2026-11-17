import asyncio, sys, os
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath(sys.argv[1]); OUT=sys.argv[2]; LANG=sys.argv[3]; vw,vh=map(int,sys.argv[4].split('x')); ST=sys.argv[5].split(',')
async def main():
  os.makedirs(OUT,exist_ok=True)
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for s in ST:
      ctx=await b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,has_touch=vw<vh,is_mobile=vw<vh)
      await ctx.add_init_script(f"try{{localStorage.setItem('tantan-lang','{LANG}');localStorage.setItem('tantan-save',JSON.stringify({{pname:'ぽんぽこ',nmAsked:1,unlock:2}}));localStorage.setItem('kenka-hints2','[]')}}catch(e){{}}")
      pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
      await pg.goto(URL); await pg.wait_for_timeout(2000)
      await pg.evaluate(f"()=>{{openMenu(); mDo('{s}')}}")
      for t,nm in [(1200,'a'),(3500,'b'),(6000,'c')]:
        await pg.wait_for_timeout(t if nm=='a' else t-prev); prev=t
        await pg.screenshot(path=f'{OUT}/{s}_{nm}.png')
      # 早送り：tick を回して結果まで
      ph=await pg.evaluate("()=>{const g=window.__game; for(let i=0;i<9000&&!['tally'].includes(g.phase);i++) g.tick&&g.tick(); return g.phase}")
      await pg.wait_for_timeout(2500); await pg.screenshot(path=f'{OUT}/{s}_d.png')
      print(s,'phase',ph, errs[:2]); await ctx.close()
    await b.close()
prev=0
asyncio.run(main())
