# リカリカイ

SAKU制作のオリジナル漫画『リカリカイ』の公開サイトです（GitHub Pages）。
公開URL: https://saku3298.github.io/rikarikai/

画面はジャンププラス風です。縦向きは1ページ表示、横向きは右から左の2ページ見開きで読めます。

## フォルダ構成

| 場所 | 役割 |
|---|---|
| `work.json` | 作品情報・話数・巻・関連作品のデータ（**ここを編集します**） |
| `tools/build.py` | `work.json` から全HTMLを生成します |
| `tools/optimize_images.py` | 画像をWebPに変換して軽くします |
| `tools/make_ogp.py` | SNS共有用の画像を `images/ogp/default.jpg` に生成します |
| `css/style.css` | 画面のデザイン（トップ・ビューア・404） |
| `js/viewer.js` | ビューア（スワイプ・見開き・続きから読む） |
| `js/top.js` | トップページ（タブ切り替え・話数の並べ替え） |
| `images/episodes/` | 各話のページ画像 `episode01-001.webp` …（話2桁-ページ3桁） |
| `images/volumes/` | 単行本の表紙 `volume01-cover.webp` |
| `images/thumbs/` | 話一覧のサムネイル `episode01.webp` |
| `images/related/` | 「同じ作者の作品」の表紙 |
| `images/work/` | トップのヒーロー画像・作者画像 |
| `images/ogp/` | SNS共有用の画像（JPG） |
| `assets/favicon.svg` | タブのアイコン |
| `index.html`, `episodeN.html`, `volumeN.html`, `404.html` | **自動生成されるので直接編集しません** |

## 第2話を追加する手順

1. 画像を置く
   - 本文: `images/episodes/episode02-001.jpg`, `episode02-002.jpg` …（JPG／PNGのままで構いません）
   - サムネイル: `images/thumbs/episode02.jpg`（横長 568×216 程度）
2. `work.json` の `episodes` に追記する
   ```json
   { "no": 2, "title": "第2話のタイトル" }
   ```
   単行本にも入れる場合は、`volumes` の該当巻の `episodes` に `2` を足します（新しい巻は `images/volumes/volume02-cover.jpg` を置いて、`volumes` に追加）。
3. 変換と生成を実行する
   ```
   python3 tools/optimize_images.py --delete-originals   # WebPに変換（元のJPG/PNGは消えます）
   python3 tools/make_ogp.py                             # 共有用画像（話数の表示が変わります）
   python3 tools/build.py                                # HTML生成
   ```
   （`optimize_images.py` と `make_ogp.py` は Pillow が必要です: `pip install pillow`）
4. 変更したファイルをGitHubにアップロードする

ページ数は画像の枚数から自動で数えます。

## 操作方法

- PC: 画面の左右ボタン、← → キー、マウスホイールでページ移動
- スマートフォン縦向き: 1ページ表示・横スワイプ
- スマートフォン横向き: 右に若いページを置く2ページ見開き
- 途中で閉じても、次に開いたときに「続きから読む」を選べます（読んだ位置は読者の端末にだけ保存されます）

## GitHub Pages の公開設定

1. GitHubで `rikarikai` というPublicリポジトリを作る
2. このフォルダの**中身**をリポジトリ直下にアップロードする（フォルダごと入れない）
3. 「Settings」→「Pages」→ Source を「Deploy from a branch」、Branch を「main」、フォルダを「/ (root)」にして「Save」

## 注意

- 元の高解像度データ（PDFなど）は、GitHubとは別の場所にも保管してください。
- `index.html` などの生成物を直接編集すると、次の生成で上書きされます。
