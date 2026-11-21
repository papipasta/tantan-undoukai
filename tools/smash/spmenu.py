# 必殺技えらびの メニューを 中身入りで 日英×5サイズ 点検（python3 tools/smash/spmenu.py index.html OUT）
import asyncio, sys, os
from playwright.async_api import async_playwright

URL='file://'+os.path.abspath(sys.argv[1]); OUT=sys.argv[2]
CHECK=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','check.js')).read()
async def main():
  os.makedirs(OUT,exist_ok=True); tot=0
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for L in ['ja','en']:
     for star in [0,40]:
      for sz in ['320x568','393x852','568x320','852x393','1280x720']:
        vw,vh=map(int,sz.split('x'))
        ctx=await b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,has_touch=vw<vh,is_mobile=vw<vh)
        await ctx.add_init_script(f"try{{localStorage.setItem('tantan-lang','{L}');localStorage.setItem('tantan-save',JSON.stringify({{pname:'ぽんぽこ',nmAsked:1,unlock:2}}))}}catch(e){{}}")
        pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_timeout(1300)
        await pg.evaluate(f"()=>{{ {'for (const k of SP_KEYS) SPECIALS[k].need=()=>true;' if star else ''} openMenu(); fillSp(); mShow('mSp'); spDescFor(SP_KEYS[4]); }}"); await pg.wait_for_timeout(500)
        r=await pg.evaluate(CHECK); tot+=len(r)
        for x in r: print(L,star,sz,x)
        await pg.screenshot(path=f'{OUT}/{L}_{star}_{sz}.png'); await ctx.close()
    await b.close(); print('TOTAL',tot)
asyncio.run(main())
