# プロジェクト概要

## これは何か
テキサスホールデム初心者向けの 6-max RFI（Raise First In）レンジ学習 PWA。
ポジション別のオープンレンジを 13×13 ハンドグリッドで視覚的に学ぶ。

## 構成
- `index.html` — アプリ本体（CSS/JS インラインの単一ファイル）
- `manifest.webmanifest` — PWA マニフェスト
- `sw.js` — Service Worker（プリキャッシュ・オフライン・更新管理）
- `icons/` — アイコン群（tools/make_icons.py で生成）
- `tools/make_icons.py` — アイコン生成スクリプト（Python stdlib のみ）
- `.aidoc/` — 開発プロセス記録（_PLAN / AUDIT / REPORT / USERINPUT）

## 技術方針
- 依存ゼロ・ビルドなしの静的配信。相対パスのみでサブパス対応
- ダークフェルトテーマ。safe-area / prefers-reduced-motion / noscript 対応
- SW はバージョン定数 `VERSION` を上げて更新。トースト承認で即時反映
- ローカル確認: `python3 -m http.server 8000`

## 現状（Iteration 1 完了時点）
- HEAD: docs追加コミット（README/.aidoc整備）
- 全機能動作・全リソース配信確認済み・ブラウザプレビュー可能
