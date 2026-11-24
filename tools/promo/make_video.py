"""宣伝用ショート動画（縦 1080x1920・30fps・約30秒）を組み立てる。
前に: capture.py で 場面を 撮る（CAP）、music.py で race / royale の 曲を 書き出す（BGM_DIR に bgm_race.wav, bgm_royale.wav）
使い方: python3 tools/promo/make_video.py CAP BGM_DIR OUT.mp4 [--still 秒]   （--still は その時刻の 1コマだけ PNG で 書く）"""
import sys, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts')
CAP, BGM, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
STILL = float(sys.argv[sys.argv.index('--still') + 1]) if '--still' in sys.argv else None
W, H, FPS = 1080, 1920, 30
F_TITLE = lambda s: ImageFont.truetype(f'{FD}/ZenAntique-Regular.ttf', s)
F_MED = lambda s: ImageFont.truetype(f'{FD}/KiwiMaru-Medium.ttf', s)
F_REG = lambda s: ImageFont.truetype(f'{FD}/KiwiMaru-Regular.ttf', s)
F_VOICE = lambda s: ImageFont.truetype(f'{FD}/ZenMaruGothic-Medium.ttf', s)
NAVY, INK, GOLD, CREAM, LAV = (29, 20, 56), (18, 13, 42), (255, 210, 63), (255, 246, 226), (203, 184, 255)

def frames(name, a, b):
  return [f'{CAP}/{name}/{i:04d}.jpg' for i in range(a, b)]

# 場面: (種類, コマの 列, 上の 大見出し, 小見出し)
SCENES = [
  ('port', frames('faceoff', 30, 120), 'ライバルの 山と', 'バチバチの 運動会！'),
  ('port', frames('title', 0, 75), None, None),
  ('land', frames('hurdle', 8, 68), '障害物レース', 'だい1しゅもく'),
  ('land', frames('bread', 10, 70), 'パンくい競走', 'だい2しゅもく'),
  ('land', frames('ball', 10, 70), '大玉ころがし', 'だい3しゅもく'),
  ('land', frames('tug', 0, 60), '四方つなひき', 'だい5しゅもく'),
  ('land', frames('tama', 10, 70), '玉わり', 'だい7しゅもく'),
  ('land', frames('nawa', 10, 70), '大なわとび', 'だい8しゅもく'),
  ('land', frames('royale', 10, 100), 'バトルロワイヤル', '大トリ'),
  ('land', frames('kiri', 40, 130), 'ちゃがま だいこうしん', 'きりふだ'),
  ('land', frames('gameset', 18, 78), None, None),
  ('end', [f'{CAP}/title/0074.jpg'] * 135, None, None),
]

def ink_box(t, f):
  S = int(f.size * 4); c = Image.new('L', (S * max(1, len(t)) + S, S * 2))
  ImageDraw.Draw(c).text((S, S), t, font=f, fill=255, anchor='ls'); b = c.getbbox()
  return (b[0] - S, b[1] - S, b[2] - S, b[3] - S)

def text_c(d, cx, top, t, f, fill, stroke=0, sc=INK):
  """インクの 実寸で 左右中央・上端 そろえ"""
  bx = ink_box(t, f); w = bx[2] - bx[0]
  d.text((cx - w / 2 - bx[0], top - bx[1]), t, font=f, fill=fill, anchor='ls', stroke_width=stroke, stroke_fill=sc)
  return bx[3] - bx[1]

def fit_font(t, mk, size, maxw):
  while size > 20:
    f = mk(size); bx = ink_box(t, f)
    if bx[2] - bx[0] <= maxw: return f
    size -= 4
  return mk(size)

BUNT = None
def bunting():
  global BUNT
  if BUNT is None: BUNT = Image.open(f'{CAP}/title/0000.jpg').convert('RGB').crop((0, 0, W, 120))
  return BUNT

def ease(x): return 1 - (1 - min(1, max(0, x))) ** 3

def compose(kind, path, head, sub, k, n):
  im = Image.new('RGB', (W, H), NAVY)
  if kind == 'port':
    im.paste(Image.open(path).convert('RGB').resize((W, H), Image.LANCZOS), (0, 0))
    if head:
      d = ImageDraw.Draw(im, 'RGBA'); a = ease(k / 8)
      top = int(150 - (1 - a) * 40)   # 顔に かぶせない：上の 髪の あたりに 帯
      d.rectangle((0, top - 50, W, top + 250), fill=(18, 13, 42, int(225 * a)))
      f1 = fit_font(head, F_MED, 76, W - 160); h1 = text_c(d, W / 2, top, head, f1, CREAM)
      f2 = fit_font(sub, F_MED, 104, W - 140); text_c(d, W / 2, top + h1 + 34, sub, f2, GOLD)
    elif k < n:   # タイトル：下に ひとこと
      d = ImageDraw.Draw(im, 'RGBA'); a = ease((k - 10) / 10)
      if a > 0:
        d.rectangle((60, 1440, W - 60, 1640), fill=(18, 13, 42, int(225 * a)), outline=(255, 255, 255, int(255 * a)), width=6)
        f = F_MED(66); text_c(d, W / 2, 1500, 'ぜんぶで 11しゅもく', f, CREAM)
    return im
  if kind == 'end':
    bg = Image.open(path).convert('RGB').resize((W, H), Image.LANCZOS)
    im.paste(bg, (0, 0)); d = ImageDraw.Draw(im, 'RGBA'); a = ease(k / 10)
    y0 = int(1200 + (1 - a) * 80)   # 動画の 中の URL は 押せないので のせない
    d.rectangle((60, y0, W - 60, y0 + 400), fill=(18, 13, 42, 238), outline=(255, 255, 255), width=6)
    y = y0 + 70
    y += text_c(d, W / 2, y, 'ブラウザで すぐ あそべる', F_MED(76), GOLD) + 44
    y += text_c(d, W / 2, y, 'むりょう　スマホ・PC　日本語／English', F_REG(44), CREAM) + 64
    text_c(d, W / 2, y, '水曜日のパピィー　@cookingpapi55', F_REG(40), LAV)
    return im
  # 横画面の ゲーム：まんなかに 1080x810
  im.paste(bunting(), (0, 150))
  g = Image.open(path).convert('RGB')
  im.paste(g, (0, 620))
  d = ImageDraw.Draw(im, 'RGBA')
  d.line((0, 618, W, 618), fill=(255, 255, 255), width=4); d.line((0, 1432, W, 1432), fill=(255, 255, 255), width=4)
  if head:
    a = ease(k / 7); dy = int((1 - a) * 40)
    if sub: text_c(d, W / 2, 316 + dy, sub, F_MED(56), GOLD)
    f = fit_font(head, F_MED, 116, W - 120); text_c(d, W / 2, 400 + dy, head, f, CREAM, stroke=0)
  # 下：シリーズの しるし
  text_c(d, W / 2, 1520, 'たんたんたぬきの大運動会', F_TITLE(64), CREAM)
  return im

def render():
  if STILL is not None:
    t = 0
    for kind, fr, head, sub in SCENES:
      if STILL * FPS < t + len(fr):
        k = int(STILL * FPS - t); compose(kind, fr[k], head, sub, k, len(fr)).save(OUT); return
      t += len(fr)
    return
  os.makedirs('/tmp/promo_parts', exist_ok=True); parts = []
  for si, (kind, fr, head, sub) in enumerate(SCENES):
    out = f'/tmp/promo_parts/s{si:02d}.mp4'; tmp = out + '.part.mp4'
    if os.environ.get('KEEP') and os.path.exists(out): parts.append(out); continue
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    for k, path in enumerate(fr): p.stdin.write(compose(kind, path, head, sub, k, len(fr)).tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); parts.append(out); print('scene', si, len(fr), flush=True)
  lst = '/tmp/promo_parts/list.txt'; open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
  silent = '/tmp/promo_parts/video.mp4'
  subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', silent], check=True)
  total = sum(len(s[1]) for s in SCENES) / FPS
  cut = sum(len(s[1]) for s in SCENES[:8]) / FPS   # バトルロワイヤルから 曲を かえる
  af = (f"[1:a]atrim=0:{cut + .4},afade=t=out:st={cut}:d=0.4[a1];"
        f"[2:a]atrim=0:{total - cut},afade=t=in:d=0.15,afade=t=out:st={total - cut - 1.6}:d=1.6,adelay={int(cut * 1000)}|{int(cut * 1000)}[a2];"
        f"[a1][a2]amix=inputs=2:normalize=0,atrim=0:{total},afade=t=in:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
  subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-stream_loop', '-1', '-i', f'{BGM}/bgm_race.wav', '-stream_loop', '-1', '-i', f'{BGM}/bgm_royale.wav', '-filter_complex', af,
                  '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(total), '-movflags', '+faststart', OUT + '.part.mp4'], check=True)
  os.replace(OUT + '.part.mp4', OUT); print('done', OUT, round(total, 2), 's')

render()
