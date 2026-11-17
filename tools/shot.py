# 使い方: python3 shot.py <html> <outdir> <lang> <WxH,...>  : 各窓を開いて撮る＋はみ出し点検
import asyncio, sys, json, os
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath(sys.argv[1]); OUT=sys.argv[2]; LANG=sys.argv[3]
SIZES=[tuple(map(int,s.split('x'))) for s in sys.argv[4].split(',')]
STEPS=json.load(open(os.path.join(os.path.dirname(__file__),'steps.json')))
CHECK=open(os.path.join(os.path.dirname(__file__),'check.js')).read()
async def main():
  os.makedirs(OUT,exist_ok=True); total=0
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--autoplay-policy=no-user-gesture-required'])
    for vw,vh in SIZES:
      ctx=await b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,has_touch=vw<vh,is_mobile=vw<vh)
      await ctx.add_init_script(f"try{{localStorage.setItem('tantan-lang','{LANG}');localStorage.setItem('tantan-save',JSON.stringify({{pname:'ぽんぽこ',nmAsked:1,unlock:2}}));}}catch(e){{}}")
      pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:120]))
      await pg.goto(URL); await pg.wait_for_timeout(2500)
      for nm,js,wait in STEPS:
        try: await pg.evaluate(js)
        except Exception as e: print('STEPERR',vw,vh,nm,str(e)[:100]); continue
        await pg.wait_for_timeout(wait)
        await pg.screenshot(path=f'{OUT}/{vw}x{vh}_{nm}.png')
        for x in await pg.evaluate(CHECK): print(f'{vw}x{vh} {nm}: {x}'); total+=1
      for e in errs[:3]: print('JSERR',vw,vh,e)
      await ctx.close()
    await b.close()
  print('TOTAL',total)
asyncio.run(main())
