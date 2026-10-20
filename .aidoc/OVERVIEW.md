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

## 現状（Iteration 3 完了時点）
- **公開中（2系統）**:
  - GitHub Pages: https://ririumu.github.io/poker_6max_rfi_range_grid/（pushで自動）
  - Netlify: https://rfi-range-grid.netlify.app（`make deploy-netlify` で手動、
    netlify.toml で git連携にも対応可）
- リポジトリ: https://github.com/ririumu/poker_6max_rfi_range_grid（public）
- Netlify サイトIDは `.netlify/state.json`（gitignore・ローカル状態）
- tools/: make_icons / bump_version / check_deploy / deploy_netlify（全て stdlib）
