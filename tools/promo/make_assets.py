"""ストア・配布用の 画像を そろえる（release/ に 書き出す）。
前に capture.py で 撮っておく:
  /tmp/cap       … 動画用（faceoff・title）
  /tmp/ogp /tmp/ogp_en … LAND=1200x630x1 の titleL（日・英）
  /tmp/cov       … LAND=630x500x2 の titleL
  /tmp/shot_ja /tmp/shot_en … LAND=1280x720x1.5 の 各場面
使い方: python3 tools/promo/make_assets.py OUTDIR"""
import sys, os
from PIL import Image
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
L = Image.LANCZOS

# アイコン：オープニングの 顔アップ（あなたの たぬき）を 正方形に
fo = Image.open('/tmp/cap/faceoff/0080.jpg').convert('RGB')
ic = fo.crop((30, 1000, 950, 1920))
for n in (1024, 512, 180, 64):
  ic.resize((n, n), L).save(f'{OUT}/icon-{n}.png', optimize=True)

# カバー（itch 630x500）と OGP（1200x630）
Image.open('/tmp/cov/titleL/0039.jpg').convert('RGB').resize((630, 500), L).save(f'{OUT}/cover-630x500.png', optimize=True)
Image.open('/tmp/cov/titleL/0039.jpg').convert('RGB').save(f'{OUT}/cover-1260x1000.png', optimize=True)
Image.open('/tmp/ogp/titleL/0039.jpg').convert('RGB').save(f'{OUT}/ogp-1200x630-ja.png', optimize=True)
Image.open('/tmp/ogp_en/titleL/0039.jpg').convert('RGB').save(f'{OUT}/ogp-1200x630-en.png', optimize=True)

# スクリーンショット（1920x1080）
PICK = {
  'ja': [('hurdle', 40, '01-hurdle'), ('bread', 40, '02-bread'), ('tama', 65, '03-tamawari'), ('royale', 15, '04-royale'),
         ('kiri', 0, '05-final-ace'), ('kiri', 65, '06-chagama-parade'), ('gameset', 40, '07-game-set')],
  'en': [('hurdle', 40, '01-hurdle'), ('tug', 15, '02-tug-of-war'), ('royale', 79, '03-royale'), ('kiri', 0, '04-final-ace'),
         ('kiri', 65, '05-teakettle-parade'), ('gameset', 40, '06-game-set')],
}
for lang, picks in PICK.items():
  for sc, i, nm in picks:
    Image.open(f'/tmp/shot_{lang}/{sc}/{i:04d}.jpg').convert('RGB').save(f'{OUT}/shot-{lang}-{nm}.jpg', quality=92)
# 縦（スマホ）
Image.open('/tmp/cap/title/0074.jpg').convert('RGB').save(f'{OUT}/shot-ja-00-title-phone.jpg', quality=92)
Image.open('/tmp/cap/faceoff/0080.jpg').convert('RGB').save(f'{OUT}/shot-ja-08-faceoff-phone.jpg', quality=92)
print(sorted(os.listdir(OUT)))
