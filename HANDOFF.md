# たんたんたぬきの大運動会 — 引き継ぎ

## いまの最新
- 公開先: アーティファクト f899f4ed-edc6-4c0f-9363-ae783940ea61（v99, version 1795511476-5923）
- 公開のしかた: list_files → publish_files（index.html をディスクから。edit_version より楽）
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

## v91 で足したこと（バトルロワイヤル＝スマブラふう）
- SMASH()=royale（タッグ戦も）。hit で hp ではなく f.pct が たまる。knock 時 launch() で ％に比例して ふっとぶ（f.fly）
- 場外げきつい: fly 中に koA()/koB()（リング±26、かべの内側40）を こえたら smashKO()。のこり STOCK=3、0で out
- げきつい後 f.gone=80（st='fall'で かくす）→ respawn() 空から。％の高い子は jab 以外でも knock（90%〜）
- ためスマッシュ: jab を ながおし（inp.ph）→ act 'charge'→'smash'。AI と オートは inp.sm で ためる
- 必殺技 doron（★4）・jizo（★9）。rivSp() で ライバルも 名前ハッシュで 使う。jizoCounter は hit の先頭
- HUD: hudPct()、頭の札に ％（slotTag）、カードは「％　のこりN」。制限 royale 100秒・tag 90秒、STAR_T 調整
- 検査: python3 tools/smash/sim.py index.html p10 3（AIで試合を回す）、tools/smash/shot_sm.py（必殺技を出して撮る）。test/season.js は v90 から 行番号ずれで こわれている

## v92 で足したこと（大トリの 山場）
- きりふだ玉 KIRI：stepKiri（kiriCD 18秒→以後22〜32秒ごと）。resolveHits で たたく→kiriHit→3回で f.kiri
- さいごの きりふだ：doSpecial の先頭で f.kiri なら startFinal。FINAL.ph 'cut'（75f、tick を とめる・drawFinalCut）→'go'（stepFinal、ちゃがま5列を dl に まぜて drawFinal(i)）
- GAME SET／TIME UP：GSET（drawGameSet）、決着で slowmo 100、カメラは lastKO へ。％は 殴られると ゆれる（pctShk）
- 撮る: python3 tools/smash/shot_final.py index.html OUT ja 852x393,393x852

## v93 リング
- RING は はじめから a=RING0(44)。RING_AT=[25,45,65]秒の 3秒前に 予告（RING.warn、つぎの はしを 点線＋うすい橙）→ RING_STEP(56)ずつ ちぢむ
- SMASH では 歩いている子は リングの はしで とまる（physics の クランプ）。とばされた子（f.fly）だけ 外へ → koA/koB＝リング±24 で げきつい
- アイテムの 落下も リングの内側。きりふだ玉の 初回は 30秒（リング予告と 実況が かぶらないよう）
- 撮る: python3 tools/smash/shot_ring.py index.html OUT ja 852x393
- 必殺技メニューの点検（runall は中身なしで開くので別に回す）: python3 tools/smash/spmenu.py index.html OUT → TOTAL 0

## 数字の目安（調整の前後で比べる）
- python3 tools/smash/stats.py index.html p10 10 → 試合の長さ・決着・リング段・げきつい％・きりふだ玉の 出現/ゲット/発動
- v93 の基準（10本）: 平均82.6秒（52〜110）、GAME SET 7 / TIME UP 3、げきつい10/試合、げきつい時の％ 中央103（11〜208）、玉 出現15・ゲット9・発動4
- v94（10本）: リング RING_AT 65→60秒。launch の vx に倍率：リング2段目以降で ％<70 は ×0.72（早落ちを へらす）、3段目以降で ％≥70 は ×1.18（終盤を しめる）
  → 平均82.6秒、GAME SET 8 / TIME UP 2、リング3段まで 8本、げきつい時の％ 中央103.5

## v95 オープニングの 顔アップ（線が あれる → 直した）
- ふだんの絵は BK=0.5（540²）で 焼く。顔アップは 端末で 1画素あたり 約4倍に 引きのばすので 荒れていた
- bake(sel,col,only,bk) と tint(img,color,N)・cutCv(N)・cropCanvas(cv,bk) に 大きさを わたせるように。omPrepare で パターン1のとき A.me.hi / A.rvL.hi を bk=1（原寸1080²）で 焼き、アップは a.hi を 使う
- 元の部品が 1080² なので bk を 1 より 上げても 細かくは ならない
- 撮る: python3 tools/om_shot.py index.html OUT.png 1 330 393x852 2.75 （等倍で 切り出して 見る）

## v96 オープニングの たぬきは 毎回 くじ
- omPrepare の lk：あなた（playerLook）以外は 毎回 randomSel(Math.random) で 新しく。ライバル山は uniformOf で ユニフォームを たもつ。なかまも くじ（SAVE.mates は 使わない）
- くじの たぬき（look.once）は lookFor を 通さず bake 直接 → IndexedDB に ためない
- v97: タイトルに ならぶ 4ひき（op.lineup）も 同じく くじ。共通の randLook(ti)・segsOnce(look) を opLoad の そばに 置いた（あなた＝まんなか i=2 は playerLook）

## v98 リリース前の 点検（2026-11-24）
- メニュー runall 日英×8サイズ TOTAL 0、spmenu TOTAL 0、全11種目＋きょうのおだい を 日英で 結果まで（エラー0）
- 直した: 縦画面で カードを 出さないとき（320x568・375x667）実況の 札（#sayBar）が スティックと ボタンに かぶっていた → updBoard で パッドの いちばん上（top 6px）へ。重なりの 判定に 見えている #btns button の 上端も 入れた
- 直した: 英語の 抜け「つよい #」「おに #」を 辞書に 追加
- 道具（リポジトリの 一番上で 実行）: tools/en_miss.py（英語で 全部 開いて __trMiss を 集める）、tools/saybar.py（実況の 札と 操作部の 位置を 4サイズで 測る）、tools/first_run.py（はじめての 人の 流れを 撮る）

## v99 リリースの 仕上げ（2026-11-24）
- 直した: きろくの 窓に はじめての 人むけの ひとこと（#recEmpty）、英語「まだ」= Not yet、英語の 設定「ゆれ・ひかり」= Effects（値が 大きい字の まま 入る）、タイトルの 小見出し 2行めが 横長で 背の ひくい 画面（1200x630 など）で たぬきの 頭に かかる → 入らないときは 出さない
- 頭に description・theme-color・favicon（64）・apple-touch-icon（180）を 埋めこみ。SHARE_URL = https://papipasta.itch.io/tantan-undoukai（itch の ページ名を これに する）
- 配布物: release/（アイコン・カバー 630x500・OGP 1200x630 日英・スクショ 日英・itch 用 zip・宣伝ショート動画 30秒）
- 作りかた（tools/promo/）: capture.py（ゲームの 時計を 1コマずつ 進めて 撮る。LAND= で 横の 大きさ、LANG_=en で 英語、NMAX で コマ数）→ music.py（ゲームの BGM を WAV に）→ make_video.py（縦 1080x1920・30fps・-14 LUFS）／ make_assets.py（release/ に 画像）。書体は tools/promo/fonts/（Zen Antique・Kiwi Maru・Zen Maru Gothic）
- ストアの 文章（日英の 説明・操作表・itch の 設定値・X 告知文）は Claude の 文書「たんたんたぬきの大運動会 ストアページ一式」 https://claude.ai/artifact/XNVLidcThS8Sy3ZtLkURNR

## 次の一手
- 実機で遊んだ感想からの手直し（コウキさんの感想待ち）

## 罠
- 公開と手元の二重管理: edit_version で公開したら、同じ置換を index.html にも当てて push する
- 新しいクラウド環境ではフォルダが引き継がれない → 元ファイルは公開アーティファクトのDLで取り戻す
