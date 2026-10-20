# 6-max RFIレンジグリッド（PWA）

テキサスホールデム初心者向けに、6-max・100bb のポジション別オープンレイズレンジ（RFI: Raise First In）を 13×13 ハンドグリッドで学べる PWA アプリです。

## 機能

- UTG / HJ / CO / BTN / SB のポジション切り替え
- 13×13 ハンドグリッド（上三角=スーテッド、対角=ペア、下三角=オフスーツ）
- レンジ内ハンドを種類別に色分け（ペア=黄 / スーテッド=緑 / オフスーツ=青）
- オープン率・コンボ数の自動計算表示
- セルタップでハンド詳細（種類・コンボ数・レンジ内外）を表示
- ポジション説明・凡例・座標軸ラベル付き
- 選択ポジションを localStorage に保存
- オフライン完全動作（Service Worker プリキャッシュ）
- ホーム画面追加対応（manifest + apple-touch-icon + maskable）
- 更新時トースト通知 → タップで即時アップデート

## ファイル構成

```
index.html               単一ファイルアプリ（CSS/JS インライン）
manifest.webmanifest     PWA マニフェスト
sw.js                    Service Worker（オフライン対応・更新管理）
icons/                   アイコン類（PNG 192/512/maskable/apple-touch + SVG favicon）
tools/make_icons.py      アイコン生成スクリプト（Python 標準ライブラリのみ）
.aidoc/                  開発プロセスドキュメント
```

## 使い方

### ローカルで試す

```sh
python3 -m http.server 8000
# → http://localhost:8000
```

PWA 機能（Service Worker・インストール）は `http(s)://` 配信時のみ有効です。
`index.html` を直接ブラウザで開いてもアプリ本体は動作します。

### デプロイ

静的ファイルのみ。GitHub Pages / Netlify / Cloudflare Pages などへ
リポジトリをそのまま公開すれば動作します（相対パスのみ使用のため
サブパス配信にも対応）。

### アイコン再生成

```sh
python3 tools/make_icons.py
```

## 対応環境

- iOS Safari（ホーム画面追加・フルスクリーン対応）
- Android Chrome / Edge（インストール可能）
- デスクトップ Chrome / Edge / Safari / Firefox
- Service Worker 非対応環境でもアプリ本体は動作

## 更新のしかた

`index.html` などを変更したら `sw.js` 冒頭の `VERSION` 定数
（例: `rfi-v1` → `rfi-v2`）を上げてください。新キャッシュが配信され、
利用中の画面に更新トーストが表示されます。

## レンジデータについて

代表的な GTO 寄りの簡略レンジ。SB はレイズオンリー簡略版です
（ソルバー出力はリンプ混合戦略が一般的）。学習用途向けであり、
実戦では対戦相手・スタック・レーキに応じて調整してください。
