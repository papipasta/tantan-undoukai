import asyncio,os,json,sys
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath('index.html'); steps=json.load(open('tools/steps.json'))
async def main():
  miss=set()
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    async def page():
      ctx=await b.new_context(viewport={'width':852,'height':393})
      await ctx.add_init_script("try{localStorage.setItem('tantan-lang','en');localStorage.setItem('tantan-save',JSON.stringify({pname:'Pon',nmAsked:1,unlock:2}))}catch(e){}")
      pg=await ctx.new_page(); pg.errs=[]; pg.on('pageerror',lambda e:pg.errs.append(str(e)[:150])); await pg.goto(URL); await pg.wait_for_timeout(1500); return ctx,pg
    ctx,pg=await page()
    for nm,js,w in steps: await pg.evaluate(js); await pg.wait_for_timeout(250)
    for js in ["()=>mDo('how')"]+[f"()=>mDo('h:{i}')" for i in range(4)]+["()=>mDo('rec')","()=>mDo('r:1')","()=>mDo('spsel')","()=>mDo('wear')","()=>{mShow('mMain');mDo('diff')}"]:
      await pg.evaluate(js); await pg.wait_for_timeout(300)
    miss|=set(await pg.evaluate("()=>[...window.__trMiss]")); print('menus',pg.errs); await ctx.close()
    for st in [f'p{i}' for i in range(11)]+['daily','tut']:
      ctx,pg=await page()
      await pg.evaluate(f"()=>{{openMenu(); mDo('{st}')}}"); await pg.wait_for_timeout(1200)
      await pg.evaluate("()=>{const g=window.__game; for(let i=0;i<9000&&g.phase!=='tally';i++){g.tick&&g.tick()}}"); await pg.wait_for_timeout(1500)
      miss|=set(await pg.evaluate("()=>[...window.__trMiss]")); print(st,pg.errs); await ctx.close()
    await b.close()
  print('MISS',len(miss)); [print(' ',m) for m in sorted(miss)]
asyncio.run(main())
