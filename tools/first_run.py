import asyncio,os
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath('index.html')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    ctx=await b.new_context(viewport={'width':393,'height':852},device_scale_factor=2,has_touch=True,is_mobile=True,locale='ja-JP')
    pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:150])); pg.on('console',lambda m: m.type=='error' and errs.append('console:'+m.text[:150]))
    await pg.goto(URL); await pg.wait_for_timeout(2500); await pg.screenshot(path='tools/out_first_1.png')
    await pg.mouse.click(196,600); await pg.wait_for_timeout(1500); await pg.screenshot(path='tools/out_first_2.png')
    await pg.mouse.click(196,600); await pg.wait_for_timeout(2500); await pg.screenshot(path='tools/out_first_3.png')
    await pg.keyboard.type('たろう'); await pg.wait_for_timeout(2500); await pg.screenshot(path='tools/out_first_4.png')
    await pg.wait_for_timeout(5000); await pg.screenshot(path='tools/out_first_5.png')
    print(errs); await b.close()
asyncio.run(main())
