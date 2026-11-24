"""ゲームの BGM を そのまま WAV に 書き出す（宣伝動画の 音）。
使い方: python3 tools/promo/music.py index.html OUT.wav [場面=race]"""
import asyncio, sys, os, base64
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg = await b.new_page(); await pg.goto('file://' + os.path.abspath(sys.argv[1])); await pg.wait_for_timeout(1500)
    sc = sys.argv[3] if len(sys.argv) > 3 else 'race'
    print('styles', await pg.evaluate("()=>Object.keys(STYLES)"))
    b64 = await pg.evaluate("""async (sc)=>{ const buf = await MimiKit.render(null, curSong(), styleFor(sc), 48000);
      const n=buf.length, ch=2, out=new DataView(new ArrayBuffer(44+n*ch*2)); const W=(o,s)=>{for(let i=0;i<s.length;i++)out.setUint8(o+i,s.charCodeAt(i))};
      W(0,'RIFF'); out.setUint32(4,36+n*ch*2,true); W(8,'WAVEfmt '); out.setUint32(16,16,true); out.setUint16(20,1,true); out.setUint16(22,ch,true);
      out.setUint32(24,48000,true); out.setUint32(28,48000*ch*2,true); out.setUint16(32,ch*2,true); out.setUint16(34,16,true); W(36,'data'); out.setUint32(40,n*ch*2,true);
      const L=buf.getChannelData(0), R=buf.getChannelData(1); let o=44; for(let i=0;i<n;i++){ for(const d of [L,R]){ const v=Math.max(-1,Math.min(1,d[i])); out.setInt16(o,v*32767,true); o+=2; } }
      let s=''; const u=new Uint8Array(out.buffer); for(let i=0;i<u.length;i+=32768) s+=String.fromCharCode.apply(null,u.subarray(i,i+32768)); return btoa(s); }""", sc)
    open(sys.argv[2], 'wb').write(base64.b64decode(b64)); await b.close()
asyncio.run(main())
