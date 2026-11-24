import asyncio,os,sys
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath('index.html')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for vw,vh in [(320,568),(375,667),(360,740),(393,852)]:
      ctx=await b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,has_touch=True,is_mobile=True)
      await ctx.add_init_script("try{localStorage.setItem('tantan-lang','ja');localStorage.setItem('tantan-save',JSON.stringify({pname:'ぽんぽこ',nmAsked:1,unlock:2}))}catch(e){}")
      pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_timeout(1500)
      await pg.evaluate("()=>{openMenu();mDo('p0')}"); await pg.wait_for_timeout(2500)
      await pg.evaluate("()=>{const g=window.__game;for(let i=0;i<300;i++)g.tick()}"); await pg.wait_for_timeout(300)
      print([await pg.evaluate("()=>[...document.querySelectorAll('#btns button')].filter(e=>e.offsetParent).map(e=>e.dataset.b+(e.getBoundingClientRect().top|0))")]); print(await pg.evaluate("()=>{const b=$('board'),s=$('sayBar');const cs=getComputedStyle(b);return [b.className,cs.display,cs.visibility,cs.opacity,b.style.visibility,!!b.offsetParent,JSON.stringify(b.getBoundingClientRect()),s.style.top,s.offsetParent&&s.offsetParent.id, typeof boardEls]}")); r=await pg.evaluate("""()=>{const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'};
        const box=e=>{const r=e.getBoundingClientRect();return [r.left|0,r.top|0,r.right|0,r.bottom|0]};
        const all=[...document.querySelectorAll('body *')].filter(vis);
        const t=all.filter(e=>e.children.length<4&&/かぜ|あつさ|ごちゅうい|スタート/.test(e.textContent)&&e.textContent.length<60).map(e=>(e.id||e.className)+box(e));
        const c=all.filter(e=>/stick|btn|pad|joy/i.test(e.id+' '+e.className)).map(e=>(e.id||e.className)+box(e));
        return {t,c}}""")
      print(vw,vh,r); await pg.screenshot(path=f'tools/out_saybar_{vw}.png'); await ctx.close()
    await b.close()
asyncio.run(main())
