"""オープニングの 1場面を 撮る（画質の点検用。等倍で見る）
使い方: python3 tools/om_shot.py index.html OUT.png [パターン=1] [フレーム=330] [幅x高=393x852] [dpr=2.75]
  パターン1 = ライバルの にらみあい → 顔の アップ（330 で アップの まんなか）"""
import asyncio, sys, os
from playwright.async_api import async_playwright
URL = 'file://' + os.path.abspath(sys.argv[1]); OUT = sys.argv[2]
PAT = int(sys.argv[3]) if len(sys.argv) > 3 else 1; FR = int(sys.argv[4]) if len(sys.argv) > 4 else 330
VW, VH = map(int, (sys.argv[5] if len(sys.argv) > 5 else '393x852').split('x')); DPR = float(sys.argv[6]) if len(sys.argv) > 6 else 2.75

async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    ctx = await b.new_context(viewport={'width': VW, 'height': VH}, device_scale_factor=DPR)
    await ctx.add_init_script(f"window.__forceOM=1; window.__omPat={PAT}; try{{localStorage.setItem('tantan-lang','ja');localStorage.setItem('tantan-save',JSON.stringify({{pname:'ぽんぽこ',nmAsked:1,unlock:2}}))}}catch(e){{}}")
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    await pg.goto(URL)
    await pg.wait_for_function(f"()=>typeof OM!=='undefined'&&OM.ready&&OM.t>={FR}", timeout=60000, polling=16)
    await pg.screenshot(path=OUT)
    print('cv2', await pg.evaluate("()=>[op.cv2.width,op.cv2.height,op.S]"), 'errs', errs)
    await b.close()
asyncio.run(main())
