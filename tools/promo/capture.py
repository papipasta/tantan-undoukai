"""宣伝動画の素材を撮る。ゲームの時計を こちらで 1コマずつ 進めて、JPEG を 連番で 書き出す（コマ落ちなし）。
使い方（リポジトリの 一番上で）: python3 tools/promo/capture.py index.html OUTDIR [場面名…]
  LAND=1280x720x1.5 で 横画面の 大きさを かえる（ストア用の スクショ）。LANG_=en で 英語
場面は SCENES に 書く。横画面 480x360 × 2.25 = 1080x810 で 撮る。オープニングの 顔アップは 縦 360x640 × 3 = 1080x1920（縦動画の まんなかに 置く）。
画面の 操作ボタンは かくす。あなたの たぬきは 簡単な 自動操作（BOT）で 動かす。"""
import asyncio, sys, os, json
from playwright.async_api import async_playwright

URL = 'file://' + os.path.abspath(sys.argv[1]); OUT = sys.argv[2]; ONLY = sys.argv[3:]
FPS = 30

# 名前: (はじめる JS, 撮る前に 進める ゲーム内フレーム, 撮る コマ数, 縦か横, 付け足し JS)
SCENES = {
  'title':   ("()=>{}", 140, 90, 'port', ''),
  'titleL':  ("()=>{}", 140, 90, 'land', ''),
  'faceoff': ("()=>{}", 200, 150, 'port', 'om1'),
  'hurdle':  ("()=>{openMenu(); mDo('p0')}", 260, 80, 'land', ''),
  'bread':   ("()=>{openMenu(); mDo('p1')}", 520, 80, 'land', ''),
  'ball':    ("()=>{openMenu(); mDo('p2')}", 420, 80, 'land', ''),
  'tug':     ("()=>{openMenu(); mDo('p4')}", 260, 80, 'land', ''),
  'tama':    ("()=>{openMenu(); mDo('p6')}", 520, 80, 'land', ''),
  'nawa':    ("()=>{openMenu(); mDo('p7')}", 420, 80, 'land', ''),
  'royale':  ("()=>{openMenu(); mDo('p10')}", 900, 110, 'land', ''),
  'kiri':    ("()=>{openMenu(); mDo('p10')}", 0, 150, 'land', 'kiri'),
  'gameset': ("()=>{openMenu(); mDo('p10')}", 0, 110, 'land', 'gameset'),
}

INIT = """
(()=>{ let T=0, q=[]; window.__manual=false; const real=window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = cb => { q.push(cb); return q.length; };
  window.__step = (n, dt) => { for (let k=0;k<n;k++){ T += dt||1000/60; const c=q; q=[]; for (const f of c) { try{ f(T) }catch(e){ console.error(e) } } } };
  setInterval(()=>{ if(!window.__manual) window.__step(1, 1000/60) }, 16);
  try{ localStorage.setItem('tantan-lang', window.__lang||'ja'); localStorage.setItem('tantan-save', JSON.stringify({pname:(window.__lang==='en'?'Ponpoko':'ぽんぽこ'),nmAsked:1,unlock:2,calm:0})); localStorage.setItem('kenka-hints2', JSON.stringify(['all'])); }catch(e){}
})();"""
CSS = "#stick,#btns,#padHint,#stickZone,#btnPause,#omSkip{display:none!important}"
# あなたの たぬきの 自動操作：いちばん近い 相手へ 寄って なぐる。競走は 右へ 走って ときどき とぶ
BOT = """()=>{ const g=window.__game, P=g.player; if(!P||g.phase!=='play') return; const F=frame;
  for (const k of ['arrowleft','arrowright','arrowup','arrowdown']) keys[k]=false;
  const m=g.mode;
  if (m==='royale' || m==='tag' || m==='tama') {
    let best=null, bd=1e9; for (const f of g.fighters) { if (f===P||f.out||f.team===P.team&&f.team!=null&&m!=='royale') continue; const d=Math.abs(f.x-P.x)+Math.abs((f.z||0)-(P.z||0)); if (d<bd){bd=d;best=f;} }
    if (best) { keys[best.x>P.x?'arrowright':'arrowleft']=Math.abs(best.x-P.x)>26; if (Math.abs((best.z||0)-(P.z||0))>8) keys[(best.z||0)>(P.z||0)?'arrowdown':'arrowup']=true; }
    if (bd<70 && F%14===0) edge.p=true; if (bd<70 && F%23===0) edge.k=true; if (F%61===0) edge.j=true; if ((P.sp||0)>=SP_MAX || P.kiri) edge.s=true;
  } else { keys['arrowright']=true; tapDash.latched=true; if (F%47===0) edge.j=true; if (F%19===0) edge.p=true; }
}"""

async def shoot(b, name, lang):
  start, pre, n, orient, extra = SCENES[name]
  LV = [float(x) for x in os.environ.get('LAND', '480x360x2.25').split('x')]; vw, vh, dpr = (int(LV[0]), int(LV[1]), LV[2]) if orient == 'land' else (360, 640, 3)
  ctx = await b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=dpr, has_touch=False)
  init = INIT
  if extra.startswith('om'): init = f"window.__forceOM=1;window.__omPat={extra[2]};" + init
  await ctx.add_init_script(f"window.__lang='{lang}';" + init)
  pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
  await pg.goto(URL); await pg.add_style_tag(content=CSS)
  if extra.startswith('om'):
    await pg.wait_for_function("()=>typeof OM!=='undefined'&&OM.ready", timeout=60000)
  else:
    await pg.wait_for_timeout(2500)
  await pg.evaluate("()=>{window.__manual=true}")
  await pg.evaluate(start)
  if start != "()=>{}":
    for _ in range(80):   # 読みこみ（焼き）を 待つ。時計は 止めた まま 待つと 進まないので 少しずつ 進める
      await pg.evaluate("()=>window.__step(1)"); await pg.wait_for_timeout(25)
      if await pg.evaluate("()=>window.__game.phase==='count'||window.__game.phase==='play'"): break
  if extra == 'kiri':   # きりふだを 自分に わたして すぐ 撃つ
    await pg.evaluate("()=>window.__step(420)")
    await pg.evaluate("()=>{const P=window.__game.player; P.kiri=true; P.sp=SP_MAX; edge.s=true}")
  if extra == 'gameset':  # あなたと 1ぴきだけ のこして、撮りはじめて すぐ さいごの 1ぴきを 場外へ → GAME SET
    await pg.evaluate("()=>window.__step(500)")
    await pg.evaluate("()=>{const g=window.__game,P=g.player; const o=g.fighters.filter(f=>f!==P&&!f.out); o.slice(1).forEach(f=>{f.stock=1; smashKO(f)}); P.stock=Math.max(P.stock||1,2)}")
  step_pre = pre
  while step_pre > 0:
    k = min(60, step_pre); await pg.evaluate(BOT); await pg.evaluate(f"()=>window.__step({k})"); step_pre -= k
  os.makedirs(f'{OUT}/{name}', exist_ok=True)
  n = min(n, int(os.environ.get('NMAX', n)))
  for i in range(n):
    if extra == 'gameset' and i == 12: await pg.evaluate("()=>{const g=window.__game,P=g.player; const o=g.fighters.filter(f=>f!==P&&!f.out); o.forEach(f=>{f.stock=1; smashKO(f)})}")
    await pg.evaluate(BOT); await pg.evaluate("()=>window.__step(1)"); await pg.evaluate(BOT); await pg.evaluate("()=>window.__step(1)")
    await pg.screenshot(path=f'{OUT}/{name}/{i:04d}.jpg', type='jpeg', quality=92)
  print(name, lang, n, 'errs', errs[:2], flush=True)
  await ctx.close()

async def main():
  lang = os.environ.get('LANG_', 'ja')
  async with async_playwright() as p:
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for nm in (ONLY or SCENES): await shoot(b, nm, lang)
    await b.close()
asyncio.run(main())
