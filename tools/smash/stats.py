"""バトルロワイヤルを AI で N 本まわして、数字の調整の目安を出す。
使い方: python3 tools/smash/stats.py index.html [種目=p10] [本数=10]
出るもの: 試合の長さ・決着(GAME SET/TIME UP)・げきつい数と その時の％・リングが何段まで ちぢんだか・
          きりふだ玉の 出現/ゲット/発動・きりふだで 落ちた数。最後に平均。"""
import asyncio, sys, os, json, statistics as S
from playwright.async_api import async_playwright
URL = 'file://' + os.path.abspath(sys.argv[1]); ST = sys.argv[2] if len(sys.argv) > 2 else 'p10'
N = int(sys.argv[3]) if len(sys.argv) > 3 else 10

HOOK = """()=>{window.__S={ko:[],kiriIn:0,kiriGet:0,final:0,finalKO:0};
 const K0=smashKO; smashKO=(f)=>{window.__S.ko.push({p:f.pct|0,t:(frame/60)|0,fin:!!FINAL}); if(FINAL)window.__S.finalKO++; return K0(f)};
 const H0=kiriHit; kiriHit=(a)=>{const had=!!KIRI; H0(a); if(had&&!KIRI&&a.kiri)window.__S.kiriGet++};
 const F0=startFinal; startFinal=(f)=>{window.__S.final++; return F0(f)};}"""
RUN = """()=>{const g=window.__game, s=window.__S; let playT=0, had=false;
 for(let i=0;i<12000&&g.phase!=='tally';i++){ g.tick&&g.tick(); if(g.phase==='play')playT++;
   if(KIRI&&!had)s.kiriIn++; had=!!KIRI; }
 return {sec:+(playT/60).toFixed(1), end:GSET?GSET.k:'-', ring:RING?RING.step:0, ...s,
   left:g.fighters.filter(f=>!f.out).map(f=>f.name+':'+f.stock)}}"""

async def main():
  rows = []
  async with async_playwright() as p:
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for run in range(N):
      ctx = await b.new_context(viewport={'width': 852, 'height': 393})
      await ctx.add_init_script("try{localStorage.setItem('tantan-lang','ja');localStorage.setItem('tantan-save',JSON.stringify({pname:'ぽんぽこ',nmAsked:1,unlock:2}));localStorage.setItem('kenka-hints2','[]')}catch(e){}")
      pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
      await pg.goto(URL); await pg.wait_for_timeout(1200)
      await pg.evaluate(f"()=>{{openMenu(); mDo('{ST}')}}"); await pg.wait_for_timeout(1200)
      await pg.evaluate(HOOK); r = await pg.evaluate(RUN); r['errs'] = errs[:2]
      kp = [k['p'] for k in r['ko']]
      print(f"#{run+1:2d} {r['sec']:5.1f}秒 {r['end']:4s} リング{r['ring']}段 げきつい{len(kp):2d} ％{kp} "
            f"玉{r['kiriIn']}/ゲット{r['kiriGet']}/発動{r['final']}(落ち{r['finalKO']}) のこり{r['left']} {'ERR '+str(errs) if errs else ''}", flush=True)
      rows.append(r); await ctx.close()
    await b.close()
  allp = [k['p'] for r in rows for k in r['ko'] if not k['fin']]
  print('\n== 平均 ==')
  print('試合の長さ', round(S.mean(r['sec'] for r in rows), 1), '秒  (最短', min(r['sec'] for r in rows), '最長', max(r['sec'] for r in rows), ')')
  print('決着', {k: sum(r['end'] == k for r in rows) for k in ('set', 'time')})
  print('リング段', {k: sum(r['ring'] == k for r in rows) for k in range(4)})
  print('げきつい/試合', round(S.mean(len(r['ko']) for r in rows), 1))
  if allp: print('げきつい時の％（きりふだ以外）中央', S.median(allp), '最小', min(allp), '最大', max(allp))
  print('きりふだ玉 出現', sum(r['kiriIn'] for r in rows), 'ゲット', sum(r['kiriGet'] for r in rows), '発動', sum(r['final'] for r in rows), 'で落ちた', sum(r['finalKO'] for r in rows))
  print('エラー', sum(bool(r['errs']) for r in rows))

asyncio.run(main())
