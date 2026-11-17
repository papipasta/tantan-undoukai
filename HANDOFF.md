# たんたんたぬきの大運動会 — 引き継ぎ

## いまの最新
- 公開先: アーティファクト f899f4ed-edc6-4c0f-9363-ae783940ea61（v90, version 1794919302-7434）
- 正本: GitHub papipasta/tantan-undoukai の index.html（公開版と同一）。旧 src/ と build.py は失われた
- 新しい環境では: add_repo → git clone --depth 1 → index.html を直す → edit_version で公開 → commit/push
  → 以後は game.html を直接、アサート付き置換（python）で直す。巨大行（画像base64）は読まない
- 巨大行: awk 'length>20000' で判別。code 検索は python で len(l)<20000 の行だけ見る（grep は日本語の正規表現で落ちる）

## 季節の色の仕組み
- MKG.SEASON（1273行）: 日本時間の月日で ハロウィン10/1-31・秋11/1-30・クリスマス12/1-25
- generate()末尾: 季節中は 1/2 で季節の配色、4割で季節の柄 → 同じ名前でも月で色が変わる
- 影響するのは nameBase()（3706行）＝プレイヤーのたぬきだけ。ライバル・なかまは無関係
- 背景の seasonImg は天気（雪・雨・炎天下）の話で別物

- v89で決着: 名前のたぬきは「季節なし」で固定（generate の第3引数 noSeason=true を nameBase から渡す）
- 検査: node test/season.js index.html（11月と1月で同じ名前の見た目が一致するか）

## 点検（tools/）
- メニュー: tools/runall.sh <index.html の絶対パス> → tools の隣に log_<言語>_<サイズ>.txt（日英×8サイズ、TOTAL 0 が合格）
- 競技画面: python3 tools/game.py index.html g ja 393x852 p0 （mDo('p0') で開始→撮影→tick で結果まで）
- 一覧: python3 tools/sheet.py 'out_ja/393x852_*.png' sheet.png 7 0.5
- Chrome は /usr/bin/google-chrome を使う（playwright の同梱ブラウザは無い）

## v90 で直したこと
- 頭の「2P」札を画面内に収める／横画面の題字を万国旗の下へ／ルール札と種目札の幅をそろえる
- メインの1行目の行間、はしるボタンの字、英語の題字の倍率（測って縮める）
- fitRow: タブ・種目札・大会の札が枠に入らなければ並びごと字を下げる。英語の大会タブは Tourney、英語の種目名は2行

## 次の一手
- 実機で遊んだ感想からの手直し（コウキさんの感想待ち）

## 罠
- 公開と手元の二重管理: edit_version で公開したら、同じ置換を index.html にも当てて push する
- 新しいクラウド環境ではフォルダが引き継がれない → 元ファイルは公開アーティファクトのDLで取り戻す
