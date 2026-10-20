# プロジェクト概要

## これは何か
テキサスホールデム初心者向けの 6-max RFI（Raise First In）レンジ学習 PWA。
ポジション別のオープンレンジを 13×13 ハンドグリッドで視覚的に学ぶ。

## 構成
- `index.html` — アプリ本体（CSS/JS インラインの単一ファイル）
- `manifest.webmanifest` — PWA マニフェスト（"id":"./" で識別子安定化）
- `sw.js` — Service Worker（プリキャッシュ・オフライン・更新管理）
- `icons/` — アイコン群（tools/make_icons.py で生成）
- `Makefile` — serve / icons / bump / check / dist / clean
- `_headers` — Netlify・CF Pages 用ヘッダ（sw.js no-cache + セキュリティ）
- `.github/workflows/deploy.yml` — main push → GitHub Pages 自動デプロイ
- `tools/` — make_icons.py / bump_version.py / check_deploy.py（全て stdlib）
- `.aidoc/` — 開発プロセス記録（_PLAN / AUDIT / REPORT / USERINPUT）

## 技術方針
- 依存ゼロ・ビルドなしの静的配信。相対パスのみでサブパス対応
- 公開物は `make dist` が作る dist/ のみ（開発ドキュメントは公開しない）
- デプロイ前は check_deploy.py がゲート（ローカル・CI共通）
- リリースは `make bump` → `make dist` → push（GH Pagesなら自動公開）
- ローカル確認: `make serve`

## 現状（Iteration 2 完了時点）
- HEAD: docs更新コミット（README デプロイ手順/.aidoc整備）
- デプロイ経路: GitHub Pages(Actions) / Netlify・CF Pages(_headers) /
  任意ホスト(dist/) の3系統が整備済み
- GH Pages利用にはリポジトリ設定で Pages Source=GitHub Actions が必要
