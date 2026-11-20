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
      await pg.evaluate("()=>{const g=window.__game; for(let i=0;i<400&&g.phase!=='play';i++) g.tick(); for(let i=0;i<300;i++) g.tick();}")
      # 状況を作る：1P 87%、ライバル1 おじぞう、ライバル2 ため中、ライバル3 142%
      await pg.evaluate("""()=>{const F=window.__game.fighters, P=window.__game.player; P.pct=87; P.x=300; P.z=.55;
        const o=F.filter(f=>f!==P); o[0].x=370; o[0].z=.5; o[0].spK='jizo'; o[0].sp=100; doSpecial(o[0]);
        o[1].x=230; o[1].z=.6; o[1].pct=142; o[1].st='idle'; o[1].act=null; startAct(o[1],'charge'); o[1].act.max=999; o[1].act.t=40;
        o[2].pct=63; o[2].stock=2; P.stock=2; }""")
      await pg.wait_for_timeout(250); await pg.screenshot(path=f'{OUT}/{sz}_a.png')
      # どろん と げきつい
      await pg.evaluate("""()=>{const F=window.__game.fighters, P=window.__game.player; const o=F.filter(f=>f!==P); o[2].spK='doron'; o[2].sp=100; o[2].st='idle'; o[2].act=null; doSpecial(o[2]);
        if(o[1].act) o[1].act.max=1; }""")
      await pg.wait_for_timeout(120); await pg.screenshot(path=f'{OUT}/{sz}_b.png')
      await pg.wait_for_timeout(500); await pg.screenshot(path=f'{OUT}/{sz}_c.png')
      m=await pg.evaluate("()=>[...trMiss].slice(-40)"); print(sz, errs[:3], m); await ctx.close()
    await b.close()
asyncio.run(main())
